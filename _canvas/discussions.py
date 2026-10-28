"""Privacy line on the eight student discussions; Fail Museum consent wording. Usage: discussions.py SB-stu|CE-stu [--apply]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cv import call, get_all
from pages import COURSES

sys.stdout.reconfigure(encoding="utf-8")
label = sys.argv[1]
cid, role = COURSES[label]
APPLY = "--apply" in sys.argv
LINE = ('<p style="font-family: Arial, sans-serif; font-size: 15px; line-height: 1.6;"><strong>Before you post:</strong> no full names, school names, '
        'or private details about you or anyone else — the whole class reads this. Attach files rather than linking to an account, and if your '
        'notes touch something personal, describe it generally.</p>')
topics = get_all(f"/courses/{cid}/discussion_topics")
assert len(topics) == 8, len(topics)
for t in topics:
    msg = t["message"] or ""
    new = msg
    if "Before you post:" not in new:
        new = new.rstrip() + "\n" + LINE
    if "Fail Museum" in t["title"]:
        old = "The best exhibits get featured in the course."
        if old in new:
            new = new.replace(old, "With your OK, the best exhibits may be featured in the course (first name only).")
        assert "With your OK" in new
    if new == msg:
        print("  skip", t["title"])
        continue
    print("  would" if not APPLY else "  put ", t["title"], len(msg), "->", len(new))
    if APPLY:
        r, _ = call("PUT", f"/courses/{cid}/discussion_topics/{t['id']}", {"message": new})
        chk, _ = call("GET", f"/courses/{cid}/discussion_topics/{t['id']}")
        assert "Before you post:" in (chk["message"] or ""), t["title"]
print("done", label)
