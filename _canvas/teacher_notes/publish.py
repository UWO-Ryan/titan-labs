"""Create or update the nine Teacher Notes pages in a student course as UNPUBLISHED pages, each the first item of its
module (Read Me First sits above Module 01's own notes). Idempotent: pages are matched by exact title.
Usage: uv run --with markdown python -I publish.py SB-stu|CE-stu [--apply]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))
from build import canvas_page
from content import TITLES
from cv import call, get_all

sys.stdout.reconfigure(encoding="utf-8")
COURSES = {"SB-stu": 880098, "CE-stu": 127220000000011513}
label = sys.argv[1]
APPLY = "--apply" in sys.argv
cid = COURSES[label]

modules = get_all(f"/courses/{cid}/modules", {"include[]": ["items"]})
by_mod = {}
for m in modules:
    if m["name"][:3].startswith("M0") and m["name"][3] == " ":
        by_mod[int(m["name"][1:3])] = m
assert len(by_mod) == 8, sorted(by_mod)
pages = {p["title"]: p for p in get_all(f"/courses/{cid}/pages", {"search_term": "Teacher Notes", "per_page": 50})}
errors = 0

for n in sorted(TITLES):
    title = TITLES[n]
    html = canvas_page(n)
    mod = by_mod[1 if n == 0 else n]
    position = 1 if n != 1 else 2  # Module 01: Read Me First first, then Module 01 notes
    existing = pages.get(title)
    line = f"{label} {title}: module {mod['name'][:3]} pos {position}: page {'update' if existing else 'create'} ({len(html)} chars)"
    if not APPLY:
        print("  would", line)
        continue
    data = {"wiki_page[title]": title, "wiki_page[body]": html, "wiki_page[published]": "false", "wiki_page[editing_roles]": "teachers"}
    if existing:
        p, _ = call("PUT", f"/courses/{cid}/pages/{existing['page_id']}", data)
    else:
        p, _ = call("POST", f"/courses/{cid}/pages", data)
    chk, _ = call("GET", f"/courses/{cid}/pages/{p['page_id']}")
    ok = chk["title"] == title and not chk["published"] and (chk["body"] or "").strip() == html.strip()
    if not ok:
        errors += 1
        print("  ERROR page verify", title, chk["published"], len(chk["body"] or ""), len(html))
    items = [it for it in mod.get("items", []) if it["type"] == "Page" and it["title"] == title]
    if not items:
        it, _ = call("POST", f"/courses/{cid}/modules/{mod['id']}/items", {"module_item[type]": "Page", "module_item[page_url]": p["url"], "module_item[position]": position, "module_item[title]": title})
        items = [it]
    else:
        it = items[0]
        if it.get("position") != position:
            it, _ = call("PUT", f"/courses/{cid}/modules/{mod['id']}/items/{it['id']}", {"module_item[position]": position})
    chk_it, _ = call("GET", f"/courses/{cid}/modules/{mod['id']}/items/{it['id']}")
    pub = chk_it.get("published")
    if pub:
        errors += 1
        print("  ERROR module item is published", title)
    print("  ok   " + line + f" | item {chk_it['id']} pos {chk_it.get('position')} published={pub} url {p['url']}")

if APPLY:
    for n, m in sorted(by_mod.items()):
        items = get_all(f"/courses/{cid}/modules/{m['id']}/items")
        head = [(it["title"], it.get("published")) for it in items[:3]]
        print(f"  M{n:02d} first items: {head}")
print("DONE", label, "(applied)" if APPLY else "(dry run)", "errors:", errors)
