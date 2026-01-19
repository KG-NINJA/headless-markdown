# Headless Markdown

**Headless Markdown** is a perception-first logging system.

It watches the world quietly,  
and writes Markdown **only when the world becomes still**.

No UI.  
No AI.  
No continuous narration.

Just perception → stability → memory.

---

## What this is

Headless Markdown turns a webcam into a **headless observer**.

- Detects visual change (classical CV, no AI)
- Waits until the scene becomes stable
- Runs OCR **only at that moment**
- Appends the result to a Markdown file

The output is not a log file.  
It is **a readable, structured memory of events**.

---

## Why Markdown?

Markdown is the perfect intermediate representation.

- Human-readable
- Agent-readable
- Diff-friendly
- Git-friendly
- Obsidian-friendly

Headless Markdown does not render anything.  
It only **writes memory**.

---

## Core idea

> Do not understand the world continuously.  
> Record the world **only when it stops moving**.
> Camera
↓
Frame diff (OpenCV)
↓
Change detected
↓
Wait for stability
↓
OCR (optional, minimal)
↓
Append to Markdown


---

## Usage

### Requirements

- Python 3.10+
- OpenCV
- Tesseract OCR (optional but recommended)

```bash
pip install -r requirements.txt

Run
python rmd.py


The script will create / append to:

capture.md


Only when:

a significant visual change occurs

the scene becomes stable

Example output
---
### 2026-01-19 22:10:50
_stable_after_motion_

ERROR
DEVICE NOT READY

Design principles

No continuous OCR

No real-time narration

OCR is an exception, not the default

Failure of OCR must never stop the system

Silence is a valid state

What this is NOT

Not a monitoring dashboard

Not a surveillance system

Not a Vision AI demo

Not real-time transcription

This is perception logging, not interpretation.

Possible extensions

Keyword-triggered OCR

Region-limited OCR

Daily Markdown rotation

Agent that reads the Markdown

Multi-sensor input (audio, GPIO, etc.)

Philosophy

Headless Markdown treats perception as a background process.

The screen is optional.
Understanding is optional.
Memory is not.

License

MIT

This dramatically reduces noise and preserves meaning.

---

## How it works

