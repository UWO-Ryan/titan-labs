"""Same desired state as fix_quizzes.py, but for the CE clones, where PUT on a quiz question returns HTTP 500 (cross-shard):
each question that differs is re-created (POST with the desired name/text/answers at the same position), verified, and the
old one deleted. Usage: fix_quizzes_ce.py CE-edu|CE-stu [--apply]"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import urllib.error

from cv import call as _call, get_all
from fix_quizzes import COURSES, current_of, desired_for, fb


def call(method, path, data=None, params=None):
    try:
        return _call(method, path, data, params)
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} on {method} {path}: {e.read().decode('utf-8', 'replace')[:300]}")
        if data:
            print("    data keys:", sorted(data)[:12])
        raise

sys.stdout.reconfigure(encoding="utf-8")
label = sys.argv[1]
APPLY = "--apply" in sys.argv
cid, role = COURSES[label]
assert label.startswith("CE")
errors = 0
quizzes = sorted(get_all(f"/courses/{cid}/quizzes"), key=lambda q: q["title"])
assert len(quizzes) == 8
for quiz in quizzes:
    mod = int(re.match(r"M(\d\d)_", quiz["title"]).group(1))
    qid = quiz["id"]
    qs = sorted(get_all(f"/courses/{cid}/quizzes/{qid}/questions"), key=lambda q: (q.get("position") or 0, q["id"]))
    assert len(qs) == 6, (label, mod, len(qs))
    changed = []
    for i, q in enumerate(qs, 1):
        m = re.match(r"Q(\d)\b", q["question_name"])
        n = int(m.group(1)) if m else i
        assert n == i, (label, mod, q["question_name"], i)
        want = desired_for(role, mod, n, q)
        if want == current_of(q):
            continue
        changed.append(n)
        name, text, answers = want
        d = {"question[question_name]": name, "question[question_text]": text, "question[question_type]": q["question_type"],
             "question[points_possible]": q["points_possible"], "question[position]": i}
        for k in ("correct_comments", "incorrect_comments", "neutral_comments"):
            if q.get(k):
                d[f"question[{k}]"] = q[k]
        if answers is not None:
            assert sum(1 for _, w, _ in answers if w > 0) == 1 and all(c for _, _, c in answers), (label, mod, n)
            for j, (t, w, c) in enumerate(answers):
                d[f"question[answers][{j}][answer_text]"] = t
                d[f"question[answers][{j}][answer_weight]"] = w
                d[f"question[answers][{j}][answer_comment_html]"] = c
        if not APPLY:
            continue
        r, _ = call("POST", f"/courses/{cid}/quizzes/{qid}/questions", d)
        chk, _ = call("GET", f"/courses/{cid}/quizzes/{qid}/questions/{r['id']}")
        if current_of(chk) != want or chk["question_type"] != q["question_type"] or float(chk["points_possible"]) != float(q["points_possible"]):
            errors += 1
            print(f"  ERROR {label} M{mod:02d} Q{n}: new question {r['id']} does not match; old kept.\n     want {want!r}\n     got  {current_of(chk)!r}")
            call("DELETE", f"/courses/{cid}/quizzes/{qid}/questions/{r['id']}")
            continue
        call("DELETE", f"/courses/{cid}/quizzes/{qid}/questions/{q['id']}")
    line = f"{label} M{mod:02d} quiz {qid}: questions re-created: {changed}; shuffle {quiz.get('shuffle_answers')} -> True"
    if APPLY:
        r, _ = call("PUT", f"/courses/{cid}/quizzes/{qid}", {"quiz[shuffle_answers]": "true", "quiz[notify_of_update]": "false"})
        qs2 = sorted(get_all(f"/courses/{cid}/quizzes/{qid}/questions"), key=lambda q: (q.get("position") or 0, q["id"]))
        names = [q["question_name"] for q in qs2]
        ok = len(qs2) == 6 and names == [f"Question {k}" for k in range(1, 7)] and r.get("shuffle_answers") and float(r.get("points_possible") or 0) == 5.0
        if not ok:
            errors += 1
        line += f" | after: {names} points={r.get('points_possible')} shuffle={r.get('shuffle_answers')} {'OK' if ok else 'ERROR'}"
    print(line)
if APPLY:
    for quiz in get_all(f"/courses/{cid}/quizzes"):
        for q in get_all(f"/courses/{cid}/quizzes/{quiz['id']}/questions"):
            if q["question_type"] != "essay_question" and any(not fb(a) for a in q["answers"]):
                errors += 1; print(f"  ERROR {label} {quiz['title']} {q['question_name']}: empty feedback")
print("DONE", label, "(applied)" if APPLY else "(dry run)", "errors:", errors)
