"""Panel quiz fixes for all four courses. Every change is a FULL question update (name + text + answers with feedback),
verified by a re-read; a JSON snapshot of every question is written to qa2/quizsnap/ before anything changes.
Usage: fix_quizzes.py [--apply] [--only SB|CE|SB-edu|...]"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cv import call, get_all

sys.stdout.reconfigure(encoding="utf-8")
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
SNAP = Path(__file__).parent / "qa2" / "quizsnap"
SNAP.mkdir(parents=True, exist_ok=True)
COURSES = {"SB-edu": (880097, "edu"), "SB-stu": (880098, "stu"), "CE-edu": (127220000000011512, "edu"), "CE-stu": (127220000000011513, "stu")}

LABELS = {("stu", 7, 5): ("(From Modules 01 and 04.)", "(From this module.)"), ("edu", 2, 5): ("(From Module 01.)", "(From this module.)"),
          ("edu", 6, 5): ("(From Modules 02 and 04.)", "(From this module.)"), ("edu", 7, 5): ("(From Modules 05 and 06.)", "(From this module.)")}
FEEDBACK = {("edu", 1, 3): ("Correct. Only external verification works. This is the failure pattern from the Explore page: real journal, plausible author, dead DOI, zero hedging.",
                            "Correct. Only external verification works. The pattern to expect: real journal, plausible author, a DOI you must resolve yourself — and even real sources may not say what you asked for."),
            ("stu", 1, 2): ("Sounding sure and being right come from the same process.", "Sounding sure and being wrong come out of the same process.")}
ANSWER_TEXT = {("edu", 7, 3): ("Verify every worked solution — arithmetic and multi-step reasoning are a known weakness, and students trust worked examples specifically.",
                               "Verify every worked solution — arithmetic and multi-step work can still be silently wrong, and students trust worked examples specifically.")}
NEW_EDU_M01_Q5 = {"text": "<p>Module 01's Learn page insists that three words do not mean the same thing. Which three?</p>", "answers": [
    ("Fast, cheap, and accurate.", 0, "Speed and cost are real advantages, but the page's point is about what a polished answer does and does not prove."),
    ("Polished, detailed, and long.", 0, "Close — those are the surface features that make an answer feel trustworthy. The page's three words are what those features do not guarantee."),
    ("Impressive, useful, and trustworthy.", 100, "Correct. A confident answer can impress you, even help you, and still be wrong. Each word has to be earned separately — and only checking earns the third."),
    ("Generative, predictive, and creative.", 0, "Those describe how the technology works, not how to judge what it gives you.")]}


def fb(a):
    return a.get("comments_html") or a.get("comments") or ""


def desired_for(role, mod, n, q):
    """-> (name, text, [(text, weight, feedback)]) ; answers None for essay questions."""
    name = f"Question {n}"
    text = q["question_text"]
    if q["question_type"] == "essay_question":
        return name, text, None
    answers = [(a.get("html") or a["text"], int(a["weight"]), fb(a)) for a in q["answers"]]
    key = (role, mod, n)
    if key in LABELS:
        old, new = LABELS[key]
        assert old in text or new in text, (role, mod, n, text)
        text = text.replace(old, new)
    if key in FEEDBACK:
        old, new = FEEDBACK[key]
        assert any(old in c or new in c for _, _, c in answers), (role, mod, n, answers)
        answers = [(t, w, c.replace(old, new)) for t, w, c in answers]
    if key in ANSWER_TEXT:
        old, new = ANSWER_TEXT[key]
        assert any(t in (old, new) for t, _, _ in answers), (role, mod, n, answers)
        answers = [(new if t == old else t, w, c) for t, w, c in answers]
    if key == ("edu", 1, 5):
        text = NEW_EDU_M01_Q5["text"]
        answers = list(NEW_EDU_M01_Q5["answers"])
    return name, text, answers


def current_of(q):
    return q["question_name"], q["question_text"], (None if q["question_type"] == "essay_question" else [(a.get("html") or a["text"], int(a["weight"]), fb(a)) for a in q["answers"]])


def form_for(name, text, answers, q):
    d = {"question[question_name]": name, "question[question_text]": text}
    if answers is not None:
        ids = [a["id"] for a in q["answers"]]
        for i, (t, w, c) in enumerate(answers):
            if len(ids) == len(answers):
                d[f"question[answers][{i}][id]"] = ids[i]
            d[f"question[answers][{i}][answer_text]"] = t
            d[f"question[answers][{i}][answer_weight]"] = w
            d[f"question[answers][{i}][answer_comment_html]"] = c
    return d


errors = 0
for label, (cid, role) in (COURSES.items() if __name__ == "__main__" else []):
    if ONLY and not label.startswith(ONLY):
        continue
    quizzes = sorted(get_all(f"/courses/{cid}/quizzes"), key=lambda q: q["title"])
    assert len(quizzes) == 8, (label, len(quizzes))
    for quiz in quizzes:
        mod = int(re.match(r"M(\d\d)_", quiz["title"]).group(1))
        qid = quiz["id"]
        qs = sorted(get_all(f"/courses/{cid}/quizzes/{qid}/questions"), key=lambda q: (q.get("position") or 0, q["id"]))
        assert len(qs) == 6, (label, mod, len(qs))
        snap = SNAP / f"{label}-M{mod:02d}-{qid}.json"
        if not snap.exists():
            snap.write_text(json.dumps(qs, ensure_ascii=False, indent=1), encoding="utf-8")
        changes = []
        for i, q in enumerate(qs, 1):
            m = re.match(r"Q(\d)\b", q["question_name"])
            n = int(m.group(1)) if m else i
            assert n == i, (label, mod, q["question_name"], i)
            want = desired_for(role, mod, n, q)
            if want == current_of(q):
                continue
            changes.append(n)
            if want[2] is not None:
                assert sum(1 for _, w, _ in want[2] if w > 0) == 1 and all(c for _, _, c in want[2]), (label, mod, n, want)
            if APPLY:
                r, _ = call("PUT", f"/courses/{cid}/quizzes/{qid}/questions/{q['id']}", form_for(*want, q))
                got = current_of(r)
                if got != want:
                    r2, _ = call("GET", f"/courses/{cid}/quizzes/{qid}/questions/{q['id']}")
                    got = current_of(r2)
                if got != want:
                    errors += 1
                    print(f"  ERROR {label} M{mod:02d} Q{n}: wanted {want!r}\n     got {got!r}")
        line = f"{label} M{mod:02d} quiz {qid}: shuffle {quiz.get('shuffle_answers')} -> True; questions changed: {changes}"
        if APPLY and (not quiz.get("shuffle_answers") or changes):
            r, _ = call("PUT", f"/courses/{cid}/quizzes/{qid}", {"quiz[shuffle_answers]": "true", "quiz[notify_of_update]": "false"})
            line += f" | saved shuffle={r.get('shuffle_answers')} published={r.get('published')}"
        print(line)
    if APPLY:  # verification sweep: every quiz shuffled, every name neutral, no empty feedback
        for quiz in get_all(f"/courses/{cid}/quizzes"):
            if not quiz.get("shuffle_answers"):
                errors += 1; print(f"  ERROR {label} {quiz['title']}: shuffle off")
            for q in get_all(f"/courses/{cid}/quizzes/{quiz['id']}/questions"):
                if not re.fullmatch(r"Question \d", q["question_name"]):
                    errors += 1; print(f"  ERROR {label} {quiz['title']}: name {q['question_name']!r}")
                if q["question_type"] != "essay_question" and any(not fb(a) for a in q["answers"]):
                    errors += 1; print(f"  ERROR {label} {quiz['title']} {q['question_name']}: empty feedback")
print("DONE", "(applied)" if APPLY else "(dry run)", "errors:", errors)
