"""Canvas page helpers that respect the cross-shard trap: read by url, write and verify by page_id."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cv import call, get_all

COURSES = {"SB-edu": (880097, "edu"), "SB-stu": (880098, "stu"), "CE-edu": (127220000000011512, "edu"), "CE-stu": (127220000000011513, "stu")}


def page_items(cid):
    """'m01-p01' -> module item (title, page_url, id, module_id) for every Page item."""
    out = {}
    for m in get_all(f"/courses/{cid}/modules", {"include[]": ["items"]}):
        for it in m.get("items", []):
            if it["type"] == "Page":
                mm = re.match(r"(M\d\d)_(P\d\d)", it["title"])
                if mm:
                    it["module_id"] = m["id"]
                    out[f"{mm.group(1)}-{mm.group(2)}".lower()] = it
    return out


def edit_page(cid, item, fn, title=None, apply=True, label=""):
    """fn(body) -> new body (raise to abort). Returns the verified body."""
    p, _ = call("GET", f"/courses/{cid}/pages/{item['page_url']}")
    body = p["body"] or ""
    new = fn(body)
    changed = new != body
    new_title = title if title and title != p["title"] else None
    tag = f"{label or item['title']}: body {'changed' if changed else 'same'} ({len(body)}->{len(new)})" + (f", title -> {new_title!r}" if new_title else "")
    if not (changed or new_title):
        print("  skip", tag)
        return body
    if not apply:
        print("  would", tag)
        return new
    data = {}
    if changed:
        data["wiki_page[body]"] = new
    if new_title:
        data["wiki_page[title]"] = new_title
    call("PUT", f"/courses/{cid}/pages/{p['page_id']}", data)
    chk, _ = call("GET", f"/courses/{cid}/pages/{p['page_id']}")
    got = chk["body"] or ""
    ok = (got.strip() == new.strip()) and (not new_title or chk["title"] == new_title)
    print(("  ok   " if ok else "  WARN ") + tag + ("" if ok else f" (re-read differs: {len(got)} chars, url {chk['url']})"))
    if new_title:
        print(f"       url now {chk['url']}")
    return got
