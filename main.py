from __future__ import annotations

from pathlib import Path
import html
import re

from pipeline_transform import transform_markdown_to_lp

DEFAULT_CTA_URL = "https://buy.stripe.com/test_4gweX"
DEFAULT_CTA_TEXT = "Buy Now — Get Instant Access for $5"


def _extract_cta(markdown: str) -> tuple[str, str]:
    link_match = re.search(r"\[(.*?)\]\((https?://[^\s)]+)\)", markdown)
    if link_match:
        return link_match.group(1).strip(), link_match.group(2).strip()

    plain_url_match = re.search(r"(https?://[^\s)]+)", markdown)
    if plain_url_match:
        return DEFAULT_CTA_TEXT, plain_url_match.group(1).strip()

    return DEFAULT_CTA_TEXT, DEFAULT_CTA_URL


def markdown_to_simple_html(markdown: str, title: str = "Sellable Landing Page") -> str:
    lines = markdown.splitlines()
    html_parts: list[str] = []
    in_list = False

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue

        escaped_line = html.escape(line)

        if line.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
        elif line.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            item = html.escape(line[2:].strip())
            html_parts.append(f"<li>{item}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            linked_line = re.sub(
                r"\[(.*?)\]\((.*?)\)",
                lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{html.escape(m.group(1))}</a>',
                escaped_line,
            )
            html_parts.append(f"<p>{linked_line}</p>")

    if in_list:
        html_parts.append("</ul>")

    cta_text, cta_url = _extract_cta(markdown)
    html_parts.append(
        f"""
<section class=\"cta\">
  <h3>Ready to start making sales?</h3>
  <p>Deploy this page today and start collecting payments in minutes.</p>
  <a class=\"cta-button\" href=\"{html.escape(cta_url, quote=True)}\">{html.escape(cta_text)}</a>
</section>
""".strip()
    )

    body = "\n".join(html_parts)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{ --bg: #0f172a; --card: #111827; --text: #e5e7eb; --muted: #cbd5e1; --accent: #22c55e; --accent2: #16a34a; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(180deg, #020617, #0b1220 45%); color: var(--text); margin: 0; line-height: 1.65; }}
    main {{ max-width: 860px; margin: 32px auto; padding: 24px; }}
    .card {{ background: rgba(17, 24, 39, 0.95); border: 1px solid #1f2937; border-radius: 16px; padding: 28px; box-shadow: 0 18px 40px rgba(0,0,0,0.28); }}
    h1 {{ font-size: 2rem; line-height: 1.2; margin-bottom: 10px; }}
    h2 {{ margin-top: 1.8rem; font-size: 1.2rem; color: #93c5fd; text-transform: uppercase; letter-spacing: .02em; }}
    h3 {{ margin-top: 1.2rem; }}
    p, li {{ color: var(--muted); font-size: 1.02rem; }}
    ul {{ padding-left: 20px; }}
    a {{ color: #86efac; }}
    .cta {{ margin-top: 30px; padding: 18px; border: 1px solid #14532d; border-radius: 14px; background: #052e16; }}
    .cta p {{ margin: 8px 0 16px; color: #dcfce7; }}
    .cta-button {{ display: inline-block; background: linear-gradient(180deg, var(--accent), var(--accent2)); color: #052e16; font-weight: 700; text-decoration: none; padding: 12px 18px; border-radius: 10px; }}
  </style>
</head>
<body>
  <main>
    <div class=\"card\">
{body}
    </div>
  </main>
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
