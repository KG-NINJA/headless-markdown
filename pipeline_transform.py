from __future__ import annotations

from typing import Callable


def transform_markdown_to_lp(markdown: str, llm_call: Callable[[str], str] | None = None) -> str:
    """
    Transform raw OCR markdown into sellable markdown.

    Output format:
    ## Problem
    ## Insight
    ## Solution
    ## CTA
    """
    cleaned = " ".join(line.strip() for line in markdown.splitlines() if line.strip())
    if not cleaned:
        cleaned = "No OCR text captured."

    prompt = (
        "Convert the OCR text into a short sales narrative. "
        "Return Markdown with exactly these sections: "
        "## Problem, ## Insight, ## Solution, ## CTA. "
        "Keep it concise and actionable. OCR text: "
        f"{cleaned}"
    )

    if llm_call:
        response = llm_call(prompt).strip()
        if response:
            return response

    # Fast local fallback (works without API key)
    return (
        "## Problem\n"
        f"{cleaned}\n\n"
        "## Insight\n"
        "The captured text shows a clear pain point that blocks outcomes.\n\n"
        "## Solution\n"
        "Package this pain point into a focused offer with a fast, concrete fix.\n\n"
        "## CTA\n"
        "Buy the full solution now: https://buymeacoffee.com/yourname"
    )
