"""Render the Teacher Notes Markdown (content.py) to Canvas HTML (out/tn-N.html) and one Markdown file (out/all.md).
Run: uv run --with markdown python -I build.py"""
import re
import sys
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).parent))
from content import MODULES, PAGES, TITLES

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

BANNER = ('<div style="border-left: 6px solid #fcb414; background: #fff7db; padding: 12px 18px; margin: 0 0 18px 0;">'
          '<p style="margin: 0; font-size: 15px;"><strong>Teacher-only page.</strong> Leave it unpublished; students never see unpublished items. '
          'Drafted 2026-10-28. The Playlab facts are sourced on Read Me First; the one bracket in the parent note is your school&rsquo;s own permission step.</p></div>')
HEAD = '<p style="font-size: 13px; color: #4a5160; margin: 0 0 6px 0;">AI Ready Wisconsin for Students · Teacher Notes</p>'


def md_to_canvas(md):
    html = markdown.markdown(md, extensions=["tables", "sane_lists"])
    html = html.replace("<table>", '<table style="border-collapse: collapse; width: 100%; margin: 10px 0 16px 0;">')
    html = re.sub(r"<th>", '<th style="border: 1px solid #c7ccd4; padding: 6px 10px; text-align: left; background: #f4f5f7; vertical-align: top;">', html)
    html = re.sub(r"<td>", '<td style="border: 1px solid #c7ccd4; padding: 6px 10px; vertical-align: top;">', html)
    html = html.replace("<blockquote>", '<blockquote style="border-left: 4px solid #4a5160; margin: 10px 0; padding: 8px 16px; background: #f4f5f7;">')
    html = html.replace("<li>[ ] ", "<li>&#9744; ")  # checklist glyph; Canvas has no task lists
    html = html.replace("<h2>", '<h2 style="margin-top: 26px;">')
    assert "[ ]" not in html, "unconverted checkbox"
    return html


def canvas_page(n):
    title = TITLES[n]
    sub = "" if n == 0 else f'<p style="font-size: 15px; margin: 0 0 14px 0;">Module {n:02d}: {MODULES[n]["name"]} · lab: <strong>{MODULES[n]["lab"]}</strong> · AI: {MODULES[n]["app"]}</p>'
    return f'<div>{HEAD}<h1 style="margin: 0 0 8px 0;">{title}</h1>{sub}{BANNER}{md_to_canvas(PAGES[n])}</div>'


if __name__ == "__main__":
    allmd = []
    for n in sorted(PAGES):
        html = canvas_page(n)
        (OUT / f"tn-{n}.html").write_text(html, encoding="utf-8")
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        print(f"tn-{n}.html  {TITLES[n]}  {len(html)} chars, ~{words} words")
        allmd.append(f"# {TITLES[n]}\n\n" + PAGES[n].strip() + "\n")
    (OUT / "all.md").write_text("\n\n---\n\n".join(allmd), encoding="utf-8")
    print("all.md", sum(len(p) for p in PAGES.values()), "chars")
