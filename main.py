from __future__ import annotations

from pathlib import Path
import re

from pipeline_transform import transform_markdown_to_lp


def markdown_to_simple_html(markdown: str, title: str = "Sellable Landing Page") -> str:
    lines = markdown.splitlines()
    html_parts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("# "):
            html_parts.append(f"<h1>{line[2:].strip()}</h1>")
        elif line.startswith("## "):
            html_parts.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            html_parts.append(f"<h3>{line[4:].strip()}</h3>")
        else:
            line = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', line)
            html_parts.append(f"<p>{line}</p>")

    body = "\n".join(html_parts)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 760px; margin: 40px auto; line-height: 1.6; padding: 0 16px; }}
    h1 {{ font-size: 2rem; }}
    h2 {{ margin-top: 2rem; }}
    a {{ color: #1f6feb; }}
    .cta {{ margin-top: 28px; padding: 16px; border: 1px solid #ddd; border-radius: 12px; background: #f6f8fa; }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    input_path = Path("capture.md")
    if not input_path.exists():
        input_path = Path("examples/capture_sample.md")

    raw_markdown = input_path.read_text(encoding="utf-8")
    sellable_markdown = transform_markdown_to_lp(raw_markdown)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    sellable_path = output_dir / "sellable.md"
    html_path = output_dir / "landing_page.html"

    sellable_path.write_text(sellable_markdown + "\n", encoding="utf-8")
    html = markdown_to_simple_html(sellable_markdown, title="Auto-Generated Sales Page")
    html_path.write_text(html, encoding="utf-8")

    print(f"Input:  {input_path}")
    print(f"Output: {sellable_path}")
    print(f"Output: {html_path}")


if __name__ == "__main__":
    main()
