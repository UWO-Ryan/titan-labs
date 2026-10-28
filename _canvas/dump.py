"""Dump both CE courses (modules, pages, quizzes + questions, discussions, assignments, settings) to qa2/<course>/ for review."""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cv import call, get_all

sys.stdout.reconfigure(encoding="utf-8")
COURSES = {"educator": 127220000000011512, "student": 127220000000011513}
OUT = Path(__file__).parent / "qa2"


def to_text(h):
    h = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", h or "")
    h = re.sub(r"<iframe[^>]*src=\"([^\"]+)\"[^>]*>", r" [EMBED: \1] ", h)
    h = re.sub(r"<a[^>]*href=\"([^\"]+)\"[^>]*>([\s\S]*?)</a>", r"\2 [link: \1]", h)
    h = re.sub(r"<img[^>]*alt=\"([^\"]*)\"[^>]*>", r" [image: \1] ", h)
    h = re.sub(r"<img[^>]*>", " [image: NO ALT] ", h)
    h = re.sub(r"</?(h[1-6]|p|div|li|tr|br|ul|ol|table|section|details|summary|blockquote)[^>]*>", "\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t]+", " ", h)
    return re.sub(r"\n\s*\n+", "\n\n", h).strip()


for label, cid in COURSES.items():
    d = OUT / label
    d.mkdir(parents=True, exist_ok=True)
    course, _ = call("GET", f"/courses/{cid}", params={"include[]": ["syllabus_body", "term"]})
    settings, _ = call("GET", f"/courses/{cid}/settings")
    mods = get_all(f"/courses/{cid}/modules", {"include[]": ["items", "content_details"]})
    index = [f"# {course['name']} (Canvas course {cid})", "",
             f"default view: {course.get('default_view')} | state: {course.get('workflow_state')} | "
             f"hide final grades: {settings.get('hide_final_grades')} | restrict dates: {course.get('restrict_enrollments_to_course_dates')}", ""]
    (d / "syllabus.txt").write_text(to_text(course.get("syllabus_body") or "(no syllabus)"), encoding="utf-8")
    quizzes = {q["id"]: q for q in get_all(f"/courses/{cid}/quizzes")}
    discs = {t["id"]: t for t in get_all(f"/courses/{cid}/discussion_topics")}
    assigns = {a["id"]: a for a in get_all(f"/courses/{cid}/assignments")}
    for m in mods:
        reqs = ", ".join(f"{p.get('id')}" for p in m.get("prerequisite_module_ids", []))
        index.append(f"## {m['name']}  [{'published' if m.get('published') else 'UNPUBLISHED'}; "
                     f"require sequential: {m.get('require_sequential_progress')}; prereqs: {reqs or 'none'}; "
                     f"unlock: {m.get('unlock_at') or 'none'}]")
        for n, it in enumerate(m.get("items", []), 1):
            req = it.get("completion_requirement") or {}
            tag = f"{it['type']}"
            fname = None
            body = ""
            if it["type"] == "Page":
                p, _ = call("GET", f"/courses/{cid}/pages/{it['page_url']}")
                body = p.get("body") or ""
                fname = f"{it['page_url']}.txt"
                (d / fname).write_text(f"# {it['title']}\n(page, {'published' if p.get('published') else 'UNPUBLISHED'}, updated {p.get('updated_at','')[:10]})\n\n" + to_text(body), encoding="utf-8")
                (d / (it["page_url"] + ".html")).write_text(body, encoding="utf-8")
            elif it["type"] == "Quiz":
                q = quizzes.get(it["content_id"]) or call("GET", f"/courses/{cid}/quizzes/{it['content_id']}")[0]
                qs = get_all(f"/courses/{cid}/quizzes/{it['content_id']}/questions")
                lines = [f"# {it['title']}", f"(quiz: type {q.get('quiz_type')}, {q.get('question_count')} questions, points {q.get('points_possible')}, "
                         f"attempts {q.get('allowed_attempts')}, time limit {q.get('time_limit')}, shuffle {q.get('shuffle_answers')}, "
                         f"show correct {q.get('show_correct_answers')}, {'published' if q.get('published') else 'UNPUBLISHED'})", "",
                         "## Description", to_text(q.get("description")), ""]
                for i, qq in enumerate(qs, 1):
                    lines.append(f"## Q{i} ({qq.get('question_type')}, {qq.get('points_possible')} pt) — {qq.get('question_name')}")
                    lines.append(to_text(qq.get("question_text")))
                    for a in qq.get("answers", []):
                        mark = "✔" if a.get("weight", 0) > 0 else " "
                        lines.append(f"  [{mark}] {to_text(a.get('html') or a.get('text') or '')}" + (f"  — feedback: {to_text(a.get('comments_html') or a.get('comments') or '')}" if (a.get('comments') or a.get('comments_html')) else ""))
                    for fb in ("correct_comments", "incorrect_comments", "neutral_comments"):
                        if qq.get(fb):
                            lines.append(f"  {fb}: {to_text(qq[fb])}")
                    lines.append("")
                fname = f"quiz-{it['content_id']}.txt"
                (d / fname).write_text("\n".join(lines), encoding="utf-8")
                tag += f" ({q.get('question_count')} q)"
            elif it["type"] == "Discussion":
                t = discs.get(it["content_id"]) or call("GET", f"/courses/{cid}/discussion_topics/{it['content_id']}")[0]
                fname = f"discussion-{it['content_id']}.txt"
                (d / fname).write_text(f"# {it['title']}\n(discussion, {'published' if t.get('published') else 'UNPUBLISHED'}, graded assignment: {bool(t.get('assignment_id'))}, "
                                       f"require initial post: {t.get('require_initial_post')})\n\n" + to_text(t.get("message")), encoding="utf-8")
            elif it["type"] == "Assignment":
                a = assigns.get(it["content_id"]) or call("GET", f"/courses/{cid}/assignments/{it['content_id']}")[0]
                fname = f"assignment-{it['content_id']}.txt"
                (d / fname).write_text(f"# {it['title']}\n(assignment, {a.get('points_possible')} pts, types {a.get('submission_types')}, due {a.get('due_at')}, {'published' if a.get('published') else 'UNPUBLISHED'})\n\n" + to_text(a.get("description")), encoding="utf-8")
            elif it["type"] == "File":
                tag += f": {it.get('title')}"
            elif it["type"] == "ExternalUrl":
                tag += f": {it.get('external_url')}"
            index.append(f"{n}. {it['title']}  [{tag}; {'published' if it.get('published') else 'UNPUBLISHED'}; "
                         f"requirement: {req.get('type') or 'none'}]" + (f"  → {fname}" if fname else ""))
        index.append("")
    (d / "INDEX.md").write_text("\n".join(index), encoding="utf-8")
    print(label, "modules", len(mods), "files", len(list(d.glob('*.txt'))))
