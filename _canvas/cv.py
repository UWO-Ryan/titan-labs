"""Tiny Canvas API helper. Token comes from the CANVAS_TOKEN environment variable and is never printed."""
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://uwosh.instructure.com/api/v1"
TOKEN = os.environ["CANVAS_TOKEN"]


def call(method, path, data=None, params=None):
    url = path if path.startswith("http") else BASE + path
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    body = urllib.parse.urlencode(data, doseq=True).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.loads(r.read().decode("utf-8") or "null")
        link = r.headers.get("Link", "")
    return out, link


def get_all(path, params=None):
    items, url, params = [], path, dict(params or {}, per_page=100)
    while url:
        page, link = call("GET", url, params=params)
        params = None
        items.extend(page if isinstance(page, list) else [page])
        nxt = [p.split(";")[0].strip("<> ") for p in link.split(",") if 'rel="next"' in p]
        url = nxt[0] if nxt else None
    return items


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    method, path = sys.argv[1], sys.argv[2]
    data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    print(json.dumps(get_all(path) if method == "ALL" else call(method, path, data)[0], ensure_ascii=False, indent=1))
