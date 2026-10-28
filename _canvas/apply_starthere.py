"""Apply starthere.transform to the eight student Start Here pages. Usage: apply_starthere.py SB-stu|CE-stu [--apply]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pages import COURSES, edit_page, page_items
from starthere import transform

sys.stdout.reconfigure(encoding="utf-8")
label = sys.argv[1]
cid, role = COURSES[label]
assert role == "stu"
items = page_items(cid)
for mod in range(1, 9):
    it = items[f"m{mod:02d}-p01"]
    body = edit_page(cid, it, lambda h, m=mod: transform(m, h), apply="--apply" in sys.argv, label=f"{label} M{mod:02d} Start Here")
    assert "Step 4: Share" in body or "--apply" not in sys.argv
print("done", label)
