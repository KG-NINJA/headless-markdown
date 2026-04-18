from __future__ import annotations

from typing import Callable


MANDATORY_SECTIONS = [
    "## 1) Headline",
    "## 2) Problem",
    "## 3) Solution",
    "## 4) Benefits",
    "## 5) Example Output (Before / After)",
    "## 6) CTA",
]


def transform_markdown_to_lp(markdown: str, llm_call: Callable[[str], str] | None = None) -> str:
    """Convert raw markdown into a high-converting, $5-ready landing page draft."""
    cleaned = " ".join(line.strip() for line in markdown.splitlines() if line.strip())
    if not cleaned:
        cleaned = "No source text captured yet."

    prompt = (
        "You are a direct-response copywriter. "
        "Rewrite the input into persuasive Markdown that sells a $5 product immediately. "
        "No neutral tone. No fluff. "
        "Return exactly six sections with these headings in this order: "
        f"{', '.join(MANDATORY_SECTIONS)}. "
        "Rules: "
        "1) Headline must state pain + benefit in under 16 words. "
        "2) Problem must describe current loss (time, money, missed sales). "
        "3) Solution must describe instant transformation. "
        "4) Benefits must be bullet points with measurable time/money value. "
        "5) Example must include BEFORE and AFTER snippets. "
        "6) CTA must include a real purchase link and urgent buy-now language. "
        "Input: "
        f"{cleaned}"
    )

    if llm_call:
        response = llm_call(prompt).strip()
        if response:
            return response

    # Local fallback for immediate usage without API access.
    return (
        "## 1) Headline\n"
        "Stop Losing Buyers to Confusing Pages — Launch a Sales-Ready Landing Page in Minutes\n\n"
        "## 2) Problem\n"
        "Right now, your rough notes and OCR text are costing you sales because visitors cannot instantly see value, trust your offer, or click a clear next step. Every unclear page means lost revenue today.\n\n"
        "## 3) Solution\n"
        "This tool instantly turns raw markdown into a persuasive, conversion-focused landing page with structured sales copy and a built-in buy-now CTA so you can sell in the next 24 hours.\n\n"
        "## 4) Benefits\n"
        "- Save 2-4 hours per page by skipping manual copywriting and layout.\n"
        "- Recover lost revenue by guiding visitors to one clear paid action.\n"
        "- Launch a sellable $5 offer the same day with no design team.\n\n"
        "## 5) Example Output (Before / After)\n"
        "**Before**: \"Users hit setup errors and leave before activation.\"\n\n"
        "**After**: \"Fix setup friction fast with a proven recovery checklist — start now for $5.\"\n\n"
        "## 6) CTA\n"
        "Buy Now — Get the Instant Landing Page Pack for $5: https://buy.stripe.com/test_4gweX"
    )
