"""Student Start Here pages (8): T.I.T.A.N. replaces ChatGPT (M01-M03, M06); Step 4: Apply becomes Step 4: Share (the module
discussion) on all eight; lab nicknames in Step 3; M06 emoji/step alignment; UW Oshkosh spelling on M04.
transform(mod, body) is pure; running the file reads the qa2 dumps and writes qa2/starthere/*.html for inspection."""
import glob
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
P = 'style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 10px 0;"'
PL = 'style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0;"'
H3 = 'style="color: #000000; font-size: 20px; margin: 0 0 15px 0;"'
CARD = '<div style="background: #f5f5f5; padding: 25px; border-radius: 10px; border-top: 4px solid #ffcc00; flex: 1 1 380px; min-width: 280px;">'
STEP = '<div style="background: #ffffff; padding: 22px; border-radius: 10px; border-left: 4px solid #fcb414; flex: 1 1 260px; min-width: 240px;">'
STEP_H3 = 'style="color: #000000; font-size: 18px; margin: 0 0 12px 0;"'

TITAN_H3 = f'<h3 {H3}><span aria-hidden="true">🟢</span> You\'ll use: T.I.T.A.N. — the course\'s AI chatbot</h3>\n'
TITAN_WHAT = (f'        <p {P}><strong>What it is:</strong> T.I.T.A.N. is a general-purpose AI assistant — the same kind of technology as ChatGPT or Gemini — '
              f'with a personality and a few lab missions built in. It runs inside this course. <strong>No account needed.</strong></p>\n'
              f'        <p {P}><strong>Why we\'re using it:</strong> You can experiment with what generative AI can and can\'t do without signing up for anything. '
              f'(Personal ChatGPT or Gemini accounts need a parent\'s permission under 18 — follow your school\'s rules.)</p>\n')
WHAT_DO = {
    1: (f'        <p {P}><strong>What you\'ll do:</strong> You\'ll put AI to the test in a challenge called <em>Stump the Machine</em>.</p>\n'
        '        <ul style="color: #333333; font-size: 15px; line-height: 1.8; padding-left: 20px; margin: 0;">\n'
        '          <li>First, give AI a task you think it can handle surprisingly well.</li>\n'
        '          <li>Then turn the tables and challenge it with something difficult, ambiguous, highly specific, or something <strong>you</strong> know particularly well.</li>\n'
        '        </ul>\n'),
    2: (f'        <p {P}><strong>What you\'ll do:</strong> You\'ll choose something you find difficult or genuinely want to understand and turn T.I.T.A.N. into your personal learning coach.</p>\n'
        f'        <p {PL}>You\'ll challenge it to teach the same idea in different ways, adjust its approach based on your feedback, and then teach the idea back to Lil\' T, its hopelessly confused little sibling.</p>\n'),
    3: (f'        <p {P}><strong>What you\'ll do:</strong> You\'ll start with an intentionally weak request and improve it step by step.</p>\n'
        f'        <p {PL}>You\'ll compare the responses along the way and decide whether your changes actually made the result better.</p>\n'),
}
SHARE = {
    1: f'<p {P}>Copy your Field Notes from the lab and post your best fail in the <strong>🏛️ Fail Museum</strong> discussion: what you asked, what the AI got wrong, and how you caught it.</p>\n        <p {PL}>Then reply to one classmate: could you have caught their fail without knowing the topic?</p>',
    2: f'<p {P}>Paste your Field Notes from Teach-It-Back in the <strong>📓 Field Notes</strong> discussion: which teaching strategy actually worked for you, and where is your line between AI helping you learn and AI doing the learning?</p>\n        <p {PL}>Reply to one classmate whose strategy differed from yours.</p>',
    3: f'<p {P}>Post your Field Notes from the Genie Problem in the <strong>📓 Field Notes</strong> discussion: which single change made the biggest difference in what the genie gave you?</p>\n        <p {PL}>Reply to one classmate: steal their best move and say how you\'d use it.</p>',
    4: f'<p {P}>Post your Field Notes from the Detective Agency in the <strong>📓 Field Notes</strong> discussion: which explanation style did you trust most, and does understanding <em>why</em> an AI decided something prove it\'s right?</p>\n<p {PL}>Reply to a classmate who trusted a different detective.</p>',
    5: f'<p {P}>Hang your finished creation in <strong>🖼️ The Gallery</strong> with your Field Notes — especially the credits. Before/after pairs from Round 1 to Round 3 are the best posts.</p>\n<p {PL}>Reply to one classmate and name a creative decision they made that AI didn\'t.</p>',
    6: f'<p {P}>Paste your Field Notes from the Career Time Machine in the <strong>📓 Field Notes</strong> discussion: which claims held up when you checked the real sources, and what did the 2036 version of you do that no AI did?</p>\n        <p {PL}>Reply to a classmate who explored a career you\'ve never considered.</p>',
    7: (f'<p {P}>The lab ends with something you can actually use:</p>\n'
        '        <div style="background: #000000; padding: 16px 18px; border-radius: 8px; margin-bottom: 12px;">\n'
        '          <p style="color: #ffcc00; font-size: 16px;  line-height: 1.5; margin: 0; text-align: center;">My personal AI rules</p>\n'
        '        </div>\n'
        '        <p style="color: #333333; font-size: 14px; line-height: 1.6; margin: 0 0 10px 0;">A short set of principles for how <strong>you</strong> want to use AI — when you\'re comfortable using it, when you\'ll do the work yourself, what you\'ll never give an AI system, when you\'ll verify a result, when you\'ll tell someone you used AI, and when a human should make the final call. They don\'t have to match anyone else\'s, but you should be able to explain <strong>why you chose them.</strong></p>\n'
        '        <p style="color: #333333; font-size: 14px; line-height: 1.6; margin: 0;">Post them with your Field Notes in the <strong>📓 Field Notes</strong> discussion, then reply to a classmate who ruled differently than you on the same case.</p>'),
}
DO_RENAME = {
    1: ("In <strong>Make AI Impress You. Then Make AI Fail</strong>, you'll test an AI system", "In <strong>Stump the Machine</strong>, you'll test an AI system"),
    2: ("In the <strong>AI Learning Coach Lab</strong>, you'll choose", "In <strong>Teach-It-Back</strong>, you'll choose"),
    3: ("In the <strong>Fix the Prompt AI Lab</strong>, you'll receive", "In <strong>The Genie Problem</strong>, you'll receive"),
    4: ("In the <strong>AI Cyber Threat Investigator Lab</strong>, you'll use a UWO-developed explainable AI experience", "In <strong>The Detective Agency</strong>, you'll use a UW Oshkosh explainable-AI tool"),
    5: ("In the <strong>Creative AI Lab</strong>, you'll put generative AI to work. You'll start with an idea and use AI to help develop it into something you can see, read, hear, or experience.",
        "In <strong>The Creative Gauntlet</strong>, you'll put generative AI to work. A mystery basket picks your project; you make it with an image tool, then take three rounds of notes from the Creative Director."),
    6: ("You'll use conversational AI to explore careers or educational pathways", "In <strong>The Career Time Machine</strong>, you'll use T.I.T.A.N. to explore careers or educational pathways"),
    7: ("In the <strong>AI Judgment Lab</strong>, you'll work through", "In <strong>You Be the Judge</strong>, you'll work through"),
}


def balanced_div(h, start):
    """index just past the </div> that closes the <div at `start`."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", h[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced")


def replace_card(h, marker, opener, new):
    i = h.find(marker)
    assert i >= 0, marker
    s = h.rfind(opener, 0, i)
    assert s >= 0, opener
    e = balanced_div(h, s)
    return h[:s] + new + h[e:]


def one(h, old, new):
    assert h.count(old) == 1, (h.count(old), old[:80])
    return h.replace(old, new)


def transform(mod, h):
    if mod in (1, 2, 3):
        new = CARD + "\n        " + TITAN_H3 + TITAN_WHAT + WHAT_DO[mod] + "      </div>"
        h = replace_card(h, "You'll use: ChatGPT", CARD, new)
    if mod == 6:
        h = one(h, "You'll use: Conversational AI</h3>", "You'll use: T.I.T.A.N. — the course's AI chatbot</h3>")
        h = one(h, "You'll use an approved conversational AI tool, such as <strong>ChatGPT or Gemini</strong>, to explore careers and pathways connected to your interests.",
                "You'll use <strong>T.I.T.A.N.</strong>, the course's AI chatbot (no account needed) — or an AI tool your school provides — to explore careers and pathways connected to your interests.")
        h = one(h, "          <li>Things you might want from a future career</li>\n        </ul>\n",
                "          <li>Things you might want from a future career</li>\n        </ul>\n"
                f'        <p {P}><strong>Interests and strengths — not your name, school, or town.</strong> The lab explains why.</p>\n')
    if mod == 4:
        h = one(h, "You'll use: UWO Explainable AI cybersecurity tool", "You'll use: UW Oshkosh explainable AI cybersecurity tool")
    if mod in DO_RENAME:
        h = one(h, *DO_RENAME[mod])
    if mod <= 7:
        new = STEP + "\n        " + f'<h3 {STEP_H3}><span aria-hidden="true">💬</span> Step 4: Share</h3>\n        ' + SHARE[mod] + "\n      </div>"
        h = replace_card(h, "Step 4: Apply</h3>", STEP, new)
    else:
        s = h.find('<details style="background: #f5f5f5; padding: 20px; border-radius: 8px;">\n        <summary style="cursor: pointer; color: #000000; font-size: 18px; "><span aria-hidden="true">📂</span> Step 4: Apply')
        assert s >= 0
        e = h.find("</details>", s) + len("</details>")
        new = ('<details style="background: #f5f5f5; padding: 20px; border-radius: 8px;">\n'
               '        <summary style="cursor: pointer; color: #000000; font-size: 18px; "><span aria-hidden="true">💬</span> Step 4: Share — Show your work in the Showcase</summary>\n'
               '        <div style="margin-top: 15px;">\n'
               f'          <p {P}>The lab keeps your <strong>build log</strong> as you work — what you asked, what AI produced, what you questioned, changed, verified, rejected, and decided. That log is evidence of your AI skills.</p>\n'
               f'          <p {P}>When you\'re done, post your Capstone Notes (the lab\'s copy button) and your project in <strong>🏆 The Showcase</strong>: what you chose, where AI belonged and where it didn\'t, what you verified, and what the Examiner — T.I.T.A.N.\'s final form — ruled.</p>\n'
               f'          <p {PL}>Then celebrate two classmates\' projects with specific praise.</p>\n'
               '        </div>\n      </details>')
        h = h[:s] + new + h[e:]
    if mod == 6:
        h = one(h, '<span aria-hidden="true">👀</span> Step 2: Explore', '<span aria-hidden="true">🔍</span> Step 2: Explore')
        h = one(h, '<span aria-hidden="true">🧪</span> Step 3: Do', '<span aria-hidden="true">⚡</span> Step 3: Do')
        h = one(h, "Step 5: Check your understanding</h3>", "Step 5: Check</h3>")
        i = h.find("Step 6: Wrap up</h3>")
        assert i >= 0
        s = h.rfind(STEP, 0, i)
        e = balanced_div(h, s)
        h = h[:s] + h[e:].lstrip()
    assert "Step 4: Apply" not in h and "You'll use: ChatGPT" not in h and "ChatGPT or Gemini</strong>" not in h
    assert h.count("<div") == h.count("</div>"), (h.count("<div"), h.count("</div>"))
    return h


if __name__ == "__main__":
    out = HERE / "qa2" / "starthere"
    out.mkdir(exist_ok=True)
    for mod in range(1, 9):
        f = glob.glob(str(HERE / "qa2" / "student" / f"m{mod:02d}-p01-*.html"))[0]
        h = open(f, encoding="utf-8").read()
        new = transform(mod, h)
        (out / f"m{mod:02d}.html").write_text(new, encoding="utf-8")
        print(f"M{mod:02d}: {len(h)} -> {len(new)} chars; Step 4: Share x{new.count('Step 4: Share')}; T.I.T.A.N. x{new.count('T.I.T.A.N.')}")
