"""Student Explore/Do wrapper pages: iframe heights calibrated to the measured embed heights (desktop, 1000 px wide,
tallest scene / lab with the chat panel open, plus ~8 %), a phone line above the iframe, and an honest note about where
notes are saved. Usage: wrappers.py SB-stu|CE-stu [--apply]"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pages import COURSES, edit_page, page_items

sys.stdout.reconfigure(encoding="utf-8")
label = sys.argv[1]
cid, role = COURSES[label]
assert role == "stu"
REEL_H = {1: 2500, 2: 3550, 3: 2800, 4: 2900, 5: 2500, 6: 2950, 7: 2600, 8: 3250}
LAB_H = {1: 7300, 2: 6700, 3: 7500, 4: 7300, 5: 6700, 6: 6800, 7: 7200, 8: 6700}
PHONE = ('<p style="margin: 0 0 10px 0; font-size: 15px; color: #333333; line-height: 1.6;"><strong>On a phone?</strong> '
         '<a href="{url}" target="_blank" rel="noopener">Open {what} in a new tab</a> — it fits the screen better there.</p>\n')


def make(mod, kind):
    h_new = (REEL_H if kind == "p03" else LAB_H)[mod]
    what = "the demo" if kind == "p03" else "the lab"

    def f(h):
        m = re.search(r'<iframe src="(https://uwo-ryan\.github\.io/titan-labs/[^"]+)" width="100%" height="(\d+)"', h)
        assert m, "iframe"
        url = m.group(1)
        h = h.replace(m.group(0), f'<iframe src="{url}" width="100%" height="{h_new}"')
        if "On a phone?" not in h:
            h = h.replace(f'<iframe src="{url}"', PHONE.format(url=url, what=what) + f'<iframe src="{url}"', 1)
        old = " — everything works the same, and your progress saves even more reliably there."
        if old in h:
            h = h.replace(old, ". Everything works the same. Notes save in this browser only, so use <em>Copy my Field Notes</em> before you leave or switch devices.")
        assert h.count("On a phone?") == 1
        return h
    return f


items = page_items(cid)
for mod in range(1, 9):
    for kind in ("p03", "p04"):
        it = items[f"m{mod:02d}-{kind}"]
        edit_page(cid, it, make(mod, kind), apply="--apply" in sys.argv, label=f"{label} M{mod:02d} {kind} {it['title']}")
print("done", label)
