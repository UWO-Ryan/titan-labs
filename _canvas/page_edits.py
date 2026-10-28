"""Panel page edits (both courses): planner-voice sentences, Learn->Explore pointers, educator Do/Apply pointers and H1s,
educator rewords (failure-pattern box, arithmetic line, custom-GPT example, course name), responsive video embeds with
real titles, amber/orange colour swaps, M01 Resources consent age, student Do-page naming (title + header swap).
Usage: page_edits.py dry            -> validate every edit against the qa2 dumps
       page_edits.py SB-stu [--apply] (or SB-edu / CE-stu / CE-edu)"""
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pages import COURSES, edit_page, page_items

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent

VIDEO_STYLE = "width: 100%; max-width: 640px; height: 360px; display: block; margin: 0 auto; border: 0; border-radius: 8px;"
VIDEO_TITLES = {
    ("edu", "m01-p02"): "What this machine actually is", ("edu", "m02-p02"): "Drafting vs. deciding",
    ("edu", "m03-p02"): "How to ask for what you actually want", ("edu", "m04-p02"): "The model drafts, you decide",
    ("edu", "m05-p02"): "Why detection fails and design works", ("edu", "m06-p02"): "Bias, data, and the hard questions",
    ("edu", "m07-p02"): "Why generic AI advice fails", ("edu", "m08-p02"): "From experimenting to working differently",
    ("stu", "m06-p02"): "AI and your future", ("stu", "m07-p02"): "Responsible AI use", ("stu", "m08-p02"): "AI challenge: put it all together",
}
NICK = {1: "Stump the Machine", 2: "Teach-It-Back", 3: "The Genie Problem", 4: "The Detective Agency", 5: "The Creative Gauntlet",
        6: "The Career Time Machine", 7: "You Be the Judge", 8: "The Titan Games"}
OLD_LAB = {1: "Make AI Impress You. Then Make AI Fail.", 2: "AI Learning Coach Lab", 3: "Fix the Prompt", 4: "AI Cyber Threat Investigator",
           5: "Creative AI Lab", 6: "AI Career Explorer", 7: "AI Judgment Lab", 8: "The AI Challenge"}
REEL = {1: "What Can AI Actually Do?", 2: "Answer Machine or Learning Coach?", 3: "From Vague to Useful", 4: "Sounds Right. Is It?",
        5: "Generating Isn't Creating", 6: "Inside a Job", 7: "Can vs. Should", 8: "Start to Finish"}


def one(old, new):
    def f(h):
        assert h.count(old) == 1, (h.count(old), old[:70])
        return h.replace(old, new)
    return f


def rx(pattern, repl, n=1):
    def f(h):
        hits = re.findall(pattern, h, flags=re.S)
        assert len(hits) == n, (len(hits), pattern[:70])
        return re.sub(pattern, repl, h, flags=re.S)
    return f


def allx(old, new):
    def f(h):
        assert h.count(old) >= 1, old
        return h.replace(old, new)
    return f


def video(role, prefix):
    title = VIDEO_TITLES[(role, prefix)]

    def f(h):
        m = re.search(r'<iframe style="width: 480px; height: 300px; display: inline-block;" title="Video player for [^"]*"([^>]*)></iframe>', h)
        assert m, "video iframe"
        tag = f'<iframe style="{VIDEO_STYLE}" title="Video: {title}"{m.group(1)}></iframe>'
        if role == "edu":
            old = f'<p style="color: #555555; font-size: 15px; margin: 0;"><em>{m.group(0)}</em></p>'
            assert h.count(old) == 1, "edu video wrapper"
            h = h.replace(old, tag)
        else:
            old = f'<p style="color: #ffcc00; font-size: 20px; margin: 0 0 10px 0;" aria-label="Video embed placeholder">▶ {m.group(0)}</p>'
            assert h.count(old) == 1, "stu video wrapper"
            nbsp = '\n<p style="color: #ffffff; font-size: 14px; margin: 0;">&nbsp;</p>'
            h = h.replace(old + nbsp, tag) if (old + nbsp) in h else h.replace(old, tag)
        return h
    return f


def do_page(mod):
    old, nick = OLD_LAB[mod], NICK[mod]

    def f(h):
        m = re.search(r'<h2 style="color: #000000; font-size: 26px; margin: 0 0 6px 0;">⚡ ' + re.escape(old) + r'</h2>\n<p style="color: #000000; font-size: 15px; margin: 0;"><strong>' + re.escape(nick) + r' (\S+)</strong>', h)
        assert m, ("do header", old, nick)
        emoji = m.group(1)
        h = h.replace(m.group(0), f'<h2 style="color: #000000; font-size: 26px; margin: 0 0 6px 0;">⚡ {nick}</h2>\n<p style="color: #000000; font-size: 15px; margin: 0;"><strong>{old.rstrip(".")} {emoji}</strong>')
        t = re.findall(r'title="([^"]*) — interactive AI lab"', h)
        assert len(t) == 1, t
        h = h.replace(f'title="{t[0]} — interactive AI lab"', f'title="{nick} — interactive AI lab"')
        return h
    return f


def failure_box(h):
    old = '<p style="font-size:.78em;color:#8a6a00;margin:0 0 .5em;">The failure pattern — this is what to learn</p>'
    assert h.count(old) == 1
    h = h.replace(old, '<p style="font-size:.78em;color:#8a6a00;margin:0 0 .5em;">The failure pattern you will see on other runs — not what happened in this one</p>')
    anchor = '<strong>Confidence and accuracy are unrelated here.</strong></p></div>'
    assert h.count(anchor) == 1
    return h.replace(anchor, '<strong>Confidence and accuracy are unrelated here.</strong></p>'
                     '<p style="line-height:1.6;margin:0;color:#1a1a1a;">This run hedged and produced real citations — and still missed the brief. Treat both as the pattern: check that each source <em>exists</em> and that it <em>says what you asked for</em>.</p></div>')


EDITS = {
    # ---------------- student
    ("stu", "m01-p02"): [one("Next: Explore — See it in action</strong>", f"Next: Explore — {REEL[1]}</strong>")],
    ("stu", "m02-p02"): [one("Explore — See It in Action", f"Explore — {REEL[2]}")],
    ("stu", "m03-p02"): [one("Next: Explore — Weak request vs. better request</h3>", f"Next: Explore — {REEL[3]}</h3>")],
    ("stu", "m04-p02"): [
        one("Next: Explore — Can you spot the problem?</p>", f"Next: Explore — {REEL[4]}</p>"),
        one("You encountered this idea earlier in the course. In Module 4, you are going to turn that awareness into a practical verification habit.", "Now you'll turn that awareness into a habit."),
        one("One of the learning objectives for this module is recognizing that <em>confidence and fluency do not equal accuracy</em>.", "<em>Confidence and fluency do not equal accuracy.</em>"),
        rx(r"Module 4 specifically asks you to practice verifying AI-generated claims using <strong>appropriate independent sources</strong>, rather than assuming an[^<]*", "Practice verifying claims with an <strong>independent source</strong>, rather than assuming an AI explanation or citation proves the answer."),
    ],
    ("stu", "m05-p02"): [one("Next: Explore – From idea to creation</strong>", f"Next: Explore — {REEL[5]}</strong>")],
    ("stu", "m06-p02"): [
        one("Next: Explore — How is AI changing work?</strong>", f"Next: Explore — {REEL[6]}</strong>"),
        one("Now you'll put this way of thinking into practice. You'll look across several very different occupations and consider:", "Now you'll put this way of thinking into practice. You'll follow one real job, task by task, and consider:"),
        one(" Module 6 intentionally brings the verification skill from Module 4 into career exploration.", ""),
        video("stu", "m06-p02"),
    ],
    ("stu", "m07-p02"): [
        one("Next: Explore — What would you do?</strong>", f"Next: Explore — {REEL[7]}</strong>"),
        rx(r'<p style="color: #333333; font-size: 16px; line-height: 1\.6; margin: 0;">Module 7 specifically asks you to consider who might benefit[^<]*</p>\n?', ""),
        rx(r'<p style="color: #333333; font-size: 15px; line-height: 1\.6; margin: 15px 0 0 0;">The course plan intentionally broadens Module 7[^<]*</p>\n?', ""),
        one(" That is the central judgment skill established for Module 7.", ""),
        allx("color: #b36f00;", "color: #7a4f00;"),
        video("stu", "m07-p02"),
    ],
    ("stu", "m08-p02"): [
        one("Next: Explore — What could you build?</strong>", f"Next: Explore — {REEL[8]}</strong>"),
        one("Before you choose your own challenge, you'll look at several examples of what a final project <strong>could</strong> look like. They aren't templates you have to copy—they're possibilities designed to get you thinking.",
            "Before you choose your own challenge, you'll watch one real project from first question to final decision. It isn't a template you have to copy—it's there to get you thinking."),
        one("As you explore them, ask yourself:", "As you watch, ask yourself:"),
        rx(r" The course design specifically defines the culminating experience[^<]*", ""),
        rx(r"The course strategy intentionally leaves the project open[^<]*</p>", "The project is open on purpose: different students will make different things.</p>"),
        rx(r'The course-wide plan intentionally makes (<strong>[^<]*</strong>) the first question in the final challenge\.', r"That's why the first question in the final challenge is \1"),
        rx(r"The course's culminating objectives specifically require you to demonstrate that you can <strong>select AI appropriately for a task</strong>[^<]*", "What matters is <strong>choosing AI well for the task</strong>, not showing you can operate a product."),
        one('<p style="color: #ffffff; font-size: 14px; margin: 8px 0 0 0;">This progression is the intended skill synthesis for the final module.</p>\n', ""),
        rx(r'<p style="color: #333333; font-size: 16px; line-height: 1\.6; margin: 0 0 15px 0;">These are the reflection questions already specified[^<]*<strong>Show What You Know</strong>[^<]*</p>\n?', ""),
        one('<p style="color: #ffffff; font-size: 14px; margin: 0;">That is the key takeaway established for Module 8 in the course-wide strategy.</p>\n', ""),
        video("stu", "m08-p02"),
    ],
    ("stu", "m07-p07"): [allx("color: #f57f17;", "color: #7a4f00;")],
    ("stu", "m08-p07"): [allx("color: #f57f17;", "color: #7a4f00;")],
    ("stu", "m01-p07"): [one("OpenAI also requires parental consent for users ages 13–18.", "OpenAI also requires parental consent for users under 18.")],
    **{("stu", f"m{m:02d}-p04"): [do_page(m)] for m in range(1, 9)},
    # ---------------- educator
    ("edu", "m01-p01"): [one('>Module 01 · Start Here</p>', '>AI Ready Wisconsin for Educators · Module 01 · Start Here</p>')],
    ("edu", "m01-p02"): [
        one('<p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">That is the first objective established for this module: explain generative AI in plain language and learn to recognize its confident errors rather than either trusting or dismissing its output wholesale.</p>\n', ""),
        one("That experiment is explicitly part of this module's progression toward building your <strong>AI BS-Detector</strong>.", "That experiment feeds directly into your <strong>AI BS-Detector</strong>."),
        video("edu", "m01-p02"),
    ],
    ("edu", "m01-p03"): [failure_box, one("<em>M01_P04 — Do: AI Lab.</em>", "<em>M01_P04 — Do: Make It Impress You. Then Make It Fail.</em>")],
    ("edu", "m01-p04"): [allx("color:#6b7280", "color:#4a5160")],
    ("edu", "m02-p02"): [rx(r"Module 2 is deliberately focused on teachers’ workload[^<]*</p>", "This module is about your workload, not student AI use: find the routine work AI might help produce, so your time stays on the decisions that need your expertise.</p>"), video("edu", "m02-p02")],
    ("edu", "m03-p02"): [video("edu", "m03-p02")],
    ("edu", "m03-p03"): [one("<em>M03_P04 — Do: AI Lab.</em>", "<em>M03_P04 — Do: Fix the AI Slop.</em>")],
    ("edu", "m03-p04"): [one("<em>M03_P05 — Apply: Build a Reusable AI Workflow.</em>", "<em>M03_P05 — Apply: Build Your Prompt Library.</em>")],
    ("edu", "m03-p05"): [one(">Build a Reusable AI Prompt Workflow</h2>", ">Build Your Prompt Library</h2>")],
    ("edu", "m03-p08"): [one("Product features are not permanent. OpenAI has announced a transition away from custom GPTs toward replacement workflows, with retirement currently scheduled for December 11, 2026. That is exactly why your valuable asset should be the instructions, examples, and constraints in your recipe cards, not dependence on one vendor’s feature name.",
                             "Product features are not permanent. Example: in 2026 OpenAI retired custom GPTs (scheduled for December 2026) and moved users to a differently named replacement. That is exactly why your valuable asset should be the instructions, examples, and constraints in your recipe cards, not dependence on one vendor’s feature name.")],
    ("edu", "m04-p02"): [one("Next: Explore — Build better assessment items</strong>", "Next: Explore — Can AI build a good assessment?</strong>"), video("edu", "m04-p02")],
    ("edu", "m04-p03"): [one("<em>M04_P04 — Do: AI Lab.</em>", "<em>M04_P04 — Do: Human vs. AI Judgment.</em>")],
    ("edu", "m05-p01"): [allx("color: #b36c00;", "color: #7a4f00;")],
    ("edu", "m05-p02"): [one('<p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0;">That is the direction of this module and the purpose of the assignment-redesign artifact: ending the detection arms race and teaching redesign.</p>\n', ""), video("edu", "m05-p02")],
    ("edu", "m05-p03"): [one("<em>M05_P04 — Do: AI Lab.</em>", "<em>M05_P04 — Do: Allowed / Not Allowed / It Depends.</em>")],
    ("edu", "m05-p04"): [one("<em>M05_P05 — Apply: Establish Your Classroom Approach.</em>", "<em>M05_P05 — Apply: Redesign an Assignment.</em>")],
    ("edu", "m05-p05"): [one(">Establish Your Classroom Approach</h2>", ">Redesign an Assignment</h2>")],
    ("edu", "m06-p02"): [one(" That is exactly the goal of the Module 6 policy artifact.", " That is what your classroom policy is for."), video("edu", "m06-p02")],
    ("edu", "m06-p08"): [allx("color: #e65100;", "color: #bf360c;")],
    ("edu", "m07-p01"): [allx("color: #b36c00;", "color: #7a4f00;")],
    ("edu", "m07-p02"): [
        one("That subject-specific variation is the central reason for Module 7. This lesson moves", "This lesson moves"),
        one("That is why the final artifact in this module is not a generic AI activity. You will create", "You will create"),
        video("edu", "m07-p02"),
    ],
    ("edu", "m07-p03"): [one("<strong>Watch for:</strong> Arithmetic and multi-step reasoning are a known weakness. <strong>Verify every worked solution.</strong>",
                             "<strong>Watch for:</strong> Arithmetic and multi-step work can still be wrong — and the error is silent. <strong>Verify every worked solution.</strong>")],
    ("edu", "m08-p01"): [allx("color: #b36c00;", "color: #7a4f00;")],
    ("edu", "m08-p02"): [
        one("Module 8 explicitly asks teachers to evaluate what saved time", "This module asks you to evaluate what saved time"),
        one("These are the core pieces identified for the final AI Ready Educator Toolkit.", "These are the pieces of your AI Ready Educator Toolkit."),
        video("edu", "m08-p02"),
    ],
    ("edu", "m08-p03"): [one(">What Does an AI-Ready Teacher Actually Look Like?</h2>", ">What Does an AI-Ready Teacher Look Like?</h2>")],
    ("edu", "m08-p07"): [one("You’ve Completed AI Ready</h2>", "You’ve Completed AI Ready Wisconsin</h2>")],
    ("edu", "m08-p08"): [one("You finished AI Ready. ", "You finished AI Ready Wisconsin. ")],
}
TITLES = {**{("stu", f"m{m:02d}-p04"): f"M{m:02d}_P04 - Do: {NICK[m]}" for m in range(1, 9)},
          ("edu", "m08-p07"): "M08_P07 - You've Completed AI Ready Wisconsin"}


def apply_all(ops, h):
    for op in ops:
        h = op(h)
    return h


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "dry":
        bad = 0
        for (role, prefix), ops in EDITS.items():
            files = glob.glob(str(HERE / "qa2" / ("educator" if role == "edu" else "student") / f"{prefix}-*.html"))
            if not files:
                print("  no dump for", role, prefix); continue
            h = open(files[0], encoding="utf-8").read()
            try:
                new = apply_all(ops, h)
                print(f"  ok {role} {prefix}: {len(h)} -> {len(new)}")
            except AssertionError as e:
                bad += 1; print(f"  FAIL {role} {prefix}: {e}")
        print("dry run done; failures:", bad)
    else:
        cid, role = COURSES[mode]
        items = page_items(cid)
        for (r, prefix), ops in EDITS.items():
            if r != role:
                continue
            it = items[prefix]
            edit_page(cid, it, lambda h, ops=ops: apply_all(ops, h), title=TITLES.get((role, prefix)), apply="--apply" in sys.argv, label=f"{mode} {prefix} {it['title']}")
        print("done", mode)
