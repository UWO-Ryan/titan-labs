"""Append one captured Playlab session to _explore/captures/<page>.json.

usage: add_session.py <page> <session-id> <file with {"at", "url", "turns": [html, ...]}> [note]
Turns alternate you / ai starting from the first one passed in (slice off the welcome first).
"""
import json
import sys
from pathlib import Path

page, sid, src = sys.argv[1:4]
note = sys.argv[4] if len(sys.argv) > 4 else ""
s = json.loads(Path(src).read_text(encoding="utf-8"))
if isinstance(s, str):
    s = json.loads(s)
out = Path(__file__).parent / "captures" / f"{page}.json"
d = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {
    "page": page, "tool": "T.I.T.A.N. - Prime (Playlab cmtgeocui0tjcio0wmvdaik2i, anonymous embed)", "sessions": []}
d["sessions"] = [x for x in d["sessions"] if x["id"] != sid]
d["sessions"].append({"id": sid, "url": s["url"], "at": s["at"], **({"note": note} if note else {}),
                      "turns": [{"who": "you" if i % 2 == 0 else "ai", "html": h} for i, h in enumerate(s["turns"])]})
out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(page, [x["id"] for x in d["sessions"]], len(d["sessions"][-1]["turns"]), "turns")
