"""titan-labs page edits from the panel: M04/M06 'Apply page' pointers, M05 creative-tool paragraph, 3:1 field borders,
M01 Scene 1 word-count note, a copy button for M01 FAIL HUNT, keyboard focus in the Explore player, compact phone layout
and an 'open full page' link when framed on a narrow screen."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\rvans\OneDrive\Documents\Claude\Projects\titan-labs")
LABS = ["m01-stump-the-machine", "m02-learning-coach", "m03-genie-problem", "m04-detective-agency", "m05-creative-gauntlet",
        "m06-career-time-machine", "m07-you-be-the-judge", "m08-titan-games"]
REELS = [f"m0{i}-explore-see-it-in-action" for i in range(1, 9)]


def edit(name, pairs):
    p = ROOT / f"{name}.html"
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        assert s.count(old) == 1, (name, s.count(old), old[:70])
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")


FULLPAGE_CSS = "  .fullpage { display: none; position: sticky; top: 0; z-index: 5; background: #000000; color: #ffcc00; text-align: center; padding: 10px 14px; font-weight: bold; text-decoration: none; }\n  .fullpage:focus-visible { outline: 3px solid #ffcc00; outline-offset: -3px; }\n"
FULLPAGE_JS = '<script>(function(){try{if(window.self!==window.top&&window.innerWidth<700){var a=document.getElementById("fullpage");a.href=location.href;a.style.display="block";}}catch(e){}})();</script>\n'
FULLPAGE_A = '<a id="fullpage" class="fullpage" href="#" target="_blank" rel="noopener">Open this page full-size ↗ (it fits a phone better in its own tab)</a>\n'

# ---- labs
for name in LABS:
    p = ROOT / f"{name}.html"
    s = p.read_text(encoding="utf-8")
    assert s.count("border: 2px solid #cccccc;") == 1, name
    s = s.replace("border: 2px solid #cccccc;", "border: 2px solid #767676;")
    compact = "  @media (max-width: 700px) {\n    .panel { padding: 18px; }\n    .card { padding: 16px; }\n" + ("    .stage-body { padding: 16px 14px; }\n" if ".stage-body {" in s else "") + "  }\n"
    assert s.count("</style>") == 1 and s.count("<body>") == 1 and s.count("</body>") == 1, name
    s = s.replace("</style>", FULLPAGE_CSS + compact + "</style>")
    s = s.replace("<body>", "<body>\n" + FULLPAGE_A, 1).replace("</body>", FULLPAGE_JS + "</body>")
    p.write_text(s, encoding="utf-8")

edit("m04-detective-agency", [
    ("Paste your Field Notes into the Module 4 discussion. Next stop after this: verifying a real AI claim on the Apply page.",
     "Paste your Field Notes into the Module 4 discussion — then the practice quiz and the wrap-up."),
])
edit("m06-career-time-machine", [
    ("that you want to investigate for real on the Apply page.",
     "that you want to investigate for real — start with the Module 6 Resources page (Occupational Outlook Handbook, O*NET, My Next Move)."),
    ("Paste your Field Notes into the Module 6 discussion, then take your compass to the Apply page.",
     "Paste your Field Notes into the Module 6 discussion, then take your compass to the Module 6 Resources page."),
])
edit("m05-creative-gauntlet", [
    ('      <p>Use an approved creative AI tool — free tier only, no account should be required beyond what your teacher has approved:</p>\n'
     '      <div class="launch-row">\n'
     '        <a class="launch-btn" href="https://express.adobe.com/" target="_blank" rel="noopener">🎨 Adobe Express</a>\n'
     '        <a class="launch-btn" href="https://firefly.adobe.com/" target="_blank" rel="noopener">✨ Adobe Firefly</a>\n'
     '        <span style="font-size: 14px; color: #555555;">…or the tool your instructor listed on the Resources page</span>\n'
     '      </div>\n',
     '      <p>Use the creative tool <strong>your teacher has approved</strong>. Most Wisconsin schools provide one through a school account — <strong>do not create a personal account for this lab.</strong></p>\n'
     '      <div class="launch-row">\n'
     '        <a class="launch-btn" href="https://www.adobe.com/education/express/" target="_blank" rel="noopener">🎨 Adobe Express for Education</a>\n'
     '        <a class="launch-btn" href="https://www.canva.com/education/" target="_blank" rel="noopener">🖌️ Canva for Education</a>\n'
     '        <span style="font-size: 14px; color: #555555;">…or the tool your teacher listed on the Resources page</span>\n'
     '      </div>\n'
     '      <p style="font-size: 14.5px; color: #555555; margin-top: 14px;"><strong>No tool today?</strong> Describe your image in words to the Creative Director and sketch it on paper — the rounds and the credits still count.</p>\n'),
])
edit("m01-stump-the-machine", [
    ('so T.I.T.A.N. knows the game is on, then run at least <strong>two</strong> probes. Probe A is the one that matters most — it uses the one advantage you have: <strong>you actually know your stuff.</strong></p>\n',
     'so T.I.T.A.N. knows the game is on, then run at least <strong>two</strong> probes. Probe A is the one that matters most — it uses the one advantage you have: <strong>you actually know your stuff.</strong></p>\n'
     '      <div class="briefing">\n        <code id="brief-failhunt">M01 FAIL HUNT</code>\n        <button class="copy-btn" data-copy="brief-failhunt" type="button">📋 Copy &amp; paste into the chat</button>\n      </div>\n'),
])

# ---- reels
s = (ROOT / "m01-explore-see-it-in-action.html").read_text(encoding="utf-8")
ai = re.search(r'ai: "(<p>Great question!.*?)",\n', s).group(1)
words = re.sub(r"<[^>]+>", " ", ai).replace("—", " ").split()
print("M01 scene 1 word count:", len(words))
edit("m01-explore-see-it-in-action", [
    ("<p>Also: it bragged about the word count. It was right this time. Keep that thought.</p>",
     f"<p>Also: it bragged about its word count — and the number is wrong (count it yourself: {len(words)}). It did stay under 80. Keep that thought: even the AI's self-check is a claim.</p>"),
])
for name in REELS:
    p = ROOT / f"{name}.html"
    s = p.read_text(encoding="utf-8")
    pairs = [
        ('    d.addEventListener("click", function () { idx = i; render(); });', '    d.addEventListener("click", function () { idx = i; render("title"); });'),
        ("  function render() {\n    var s = SCENES[idx];", "  function render(focus) {\n    var s = SCENES[idx];\n    var focusNode = null;"),
        ('        b.addEventListener("click", function () { picked[idx] = j; revealed[idx] = true; render(); });',
         '        b.addEventListener("click", function () { picked[idx] = j; revealed[idx] = true; render("response"); });'),
        ('      ai.className = "bubble ai reveal-in";\n', '      ai.className = "bubble ai reveal-in";\n      ai.setAttribute("tabindex", "-1");\n      focusNode = ai;\n'),
        ('    if (window.innerWidth < 700) document.getElementById("player").scrollIntoView({ block: "start" });\n  }\n',
         '    if (window.innerWidth < 700) document.getElementById("player").scrollIntoView({ block: "start" });\n'
         '    if (focus === "response" && focusNode) { focusNode.focus({ preventScroll: window.innerWidth >= 700 }); }\n'
         '    else if (focus === "title") { var t = document.getElementById("sceneTitle"); t.setAttribute("tabindex", "-1"); t.focus({ preventScroll: window.innerWidth >= 700 }); }\n  }\n'),
        ('  document.getElementById("prevBtn").addEventListener("click", function () { if (idx > 0) { idx--; render(); } });',
         '  document.getElementById("prevBtn").addEventListener("click", function () { if (idx > 0) { idx--; render("title"); } });'),
        ('  document.getElementById("nextBtn").addEventListener("click", function () { if (idx < SCENES.length - 1 && revealed[idx]) { idx++; render(); } });',
         '  document.getElementById("nextBtn").addEventListener("click", function () { if (idx < SCENES.length - 1 && revealed[idx]) { idx++; render("title"); } });'),
        ("</style>", FULLPAGE_CSS + "  .bubble.ai:focus-visible, #sceneTitle:focus-visible { outline: 3px solid #000000; outline-offset: 3px; }\n  @media (max-width: 700px) {\n    .panel { padding: 18px; }\n    .card { padding: 16px; }\n    .player-body { padding: 14px; }\n  }\n</style>"),
        ("<body>", "<body>\n" + FULLPAGE_A),
        ("</body>", FULLPAGE_JS + "</body>"),
    ]
    for old, new in pairs:
        assert s.count(old) == 1, (name, s.count(old), old[:60])
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
print("labs + reels edited")
