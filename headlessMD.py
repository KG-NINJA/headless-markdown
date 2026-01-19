import cv2
import pytesseract
import numpy as np
from datetime import datetime
import time

# Tesseractのパス（Windowsの場合必要）
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 前フレーム保持用
prev_frame = None
STABLE_SECONDS = 1.5      # 安定してからOCRするまでの秒数
CHANGE_THRESHOLD = 25     # 差分平均値の閾値（かなり緩め）

cap = cv2.VideoCapture(0)  # 0=内蔵カメラ、またはUSBカメラの番号

last_ocr_time = 0
stable_start = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 処理を軽くするため縮小（必要に応じて）
    small = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

    if prev_frame is not None:
        # 差分計算（シンプル版）
        diff = cv2.absdiff(gray, prev_frame)
        mean_diff = np.mean(diff)

        if mean_diff > CHANGE_THRESHOLD:
            # 変化検知 → 安定待ち開始
            if stable_start is None:
                stable_start = time.time()
        else:
            # 変化なし → 安定カウント継続
            if stable_start is not None:
                if time.time() - stable_start >= STABLE_SECONDS:
                    # 安定した！ → OCR実行
                    if time.time() - last_ocr_time > 3.0:  # 連続OCR防止
                        print(f"[{datetime.now()}] 変化安定 → OCR実行")

                        # 必要ならROIだけ切り出し（ここでは全画面）
                        text = pytesseract.image_to_string(
                            gray,
                            lang='jpn+eng',          # 日本語+英語
                            config='--psm 6'         # 単一ブロック想定（状況で変える）
                        )

                        # 簡易整形（実運用ではもっと頑張る）
                        lines = [line.strip() for line in text.split('\n') if line.strip()]
                        markdown = "\n".join(lines)

                        # 保存
                        with open("capture.md", "a", encoding="utf-8") as f:
                            f.write(f"\n\n---\n**{datetime.now()}**\n\n{markdown}\n")

                        last_ocr_time = time.time()
                    stable_start = None     # リセット

    prev_frame = gray.copy()
    time.sleep(0.08)  # ≈12-15fps程度で十分

cap.release()
