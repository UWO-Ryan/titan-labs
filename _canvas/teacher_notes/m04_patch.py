"""M04 lab: wire the investigation tool, orient students to its screen, supply four fictional training emails with copy
buttons, link the guide page. Run from anywhere: uv run python -I m04_patch.py [--apply]"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
F = Path("C:/Users/rvans/OneDrive/Documents/Claude/Projects/titan-labs/m04-detective-agency.html")
h = F.read_text(encoding="utf-8")
orig = h


def one(old, new):
    global h
    assert h.count(old) == 1, (h.count(old), old[:70])
    h = h.replace(old, new)


one('xaiToolUrl: "",   // ← UWO XAI cybersecurity dashboard URL',
    'xaiToolUrl: "https://xai.mostlyharmlessscholar.com/",   // The Scholar\'s Guide to Explainable AI (set 2026-10-28)')
one(' Wraps the UWO Explainable-AI cybersecurity tool (CONFIG.xaiToolUrl — SET THIS).',
    ' Wraps the explainable-AI email tool at xai.mostlyharmlessscholar.com (CONFIG.xaiToolUrl); the four training emails below are fictional (.example domains).')

one('<p><strong>The UWO investigation tool opens in a new tab.</strong> Work each case there, then file your verdict sheets here.</p>',
    '<p><strong>The investigation tool opens in a new tab.</strong> Paste a training case into its box, pick an explanation method, press <em>Analyze Email</em> — then do the same case with the other two methods. '
    '<strong>The rule list is Reggie, the paragraph is Vera, the highlighted words are Hank.</strong> Run all three detectives on every case, then file your verdict sheet here.</p>')
one('<span style="font-size: 14px; color: #555555;">Built at UW Oshkosh — real research, real tool</span>',
    '<span style="font-size: 14px; color: #555555;">Built at UW Oshkosh — real research, real tool · <a href="https://www.mostlyharmlessscholar.com/the-scholars-guide-to-explainable-ai/" target="_blank" rel="noopener">how the three detectives work</a></span>')

EMAILS = [
    ("A", "The account alert", "Subject: URGENT: Your student account will be deactivated in 24 hours\nFrom: IT Help Desk &lt;helpdesk@schoolportal-security.example&gt;\n\nDear Student,\n\nWe detected unusual sign-in activity on your account. To avoid permanent deactivation, you must verify your password within 24 hours by clicking the secure link below:\n\nhttp://schoolportal-security.example/verify-account\n\nFailure to act will result in loss of access to all assignments and grades.\n\nThank you,\nIT Help Desk"),
    ("B", "The band trip", "Subject: Reminder: band trip permission slips due TOMORROW\nFrom: Ms. Alvarez &lt;alvarez@lincolnhs.example&gt;\n\nHi everyone,\n\nQuick reminder that permission slips for Friday's band trip are due tomorrow by 3:00 pm. If you lost yours, you can download a new copy from the school website: https://lincolnhs.example/band/trip-form\n\nBring it to the band room before 3:00 or you won't be able to ride the bus.\n\nThanks,\nMs. Alvarez"),
    ("C", "The quick favor", "Subject: Quick favor\nFrom: Principal Dawson &lt;principal.dawson.office@gmail.example&gt;\n\nHi,\n\nAre you available right now? I'm in a meeting and can't talk on the phone. I need you to pick up three $100 gift cards for a staff appreciation surprise and send me the card numbers. I'll reimburse you this afternoon. Please keep this between us so it stays a surprise.\n\nThanks,\nPrincipal Dawson\nSent from my iPhone"),
    ("D", "The scholarship", "Subject: Congratulations! You have been selected for a $2,500 scholarship\nFrom: Awards Committee &lt;awards@national-student-scholars.example&gt;\n\nDear Scholar,\n\nYour name was submitted by your school for the 2026 Future Leaders Scholarship, and you have been selected. To release the funds, reply with your full name, date of birth, Social Security number, and a photo of your student ID within 48 hours. Winners who do not respond forfeit the award.\n\nCongratulations again,\nThe Awards Committee"),
]
cards = "\n".join(
    f'      <div class="briefing">\n        <p style="margin: 0 0 6px 0; font-size: 14px;"><strong>Training case {k}: {name}</strong></p>\n        <code id="case-{k.lower()}">{body}</code>\n        <button class="copy-btn" data-copy="case-{k.lower()}" type="button">📋 Copy case {k}</button>\n      </div>'
    for k, name, body in EMAILS)
block = ('  <div class="panel light">\n    <div class="sec-head"><div class="icon-circle" aria-hidden="true">📨</div><h2>The case files</h2></div>\n    <div class="card">\n'
         '      <p><strong>Four training emails, all fictional</strong> (the people, schools and <code>.example</code> addresses do not exist). Copy one, paste it into the tool, run all three detectives. Case A is the warm-up; B and C are where the detectives disagree; D is the one to interrogate hardest.</p>\n'
         f'{cards}\n    </div>\n  </div>\n\n')
one('  <div class="stage" id="stage-case1">', block + '  <div class="stage" id="stage-case1">')

one('<p>Pick your first suspicious email in the tool. Read all three detectives\' explanations before you decide anything. Then file the sheet.</p>',
    '<p>Run <strong>Case A</strong> through all three detectives in the tool. Read every explanation before you decide anything. Then file the sheet.</p>')
one('<p>Find a case where the explanations pull in different directions — or where one detective\'s evidence feels much weaker than another\'s. Someone has to make the call. That someone is you.</p>',
    '<p>Run <strong>Case B or Case C</strong>. In these the explanations pull in different directions — or one detective\'s evidence is much weaker than another\'s. Someone has to make the call. That someone is you.</p>')
one('<p>One more case — and this time, interrogate the explanations themselves.',
    '<p>One more case — <strong>Case D</strong>, or any case you haven\'t run — and this time, interrogate the explanations themselves.')

assert h.count('data-copy="case-') == 4 and h.count('id="case-') == 4
if "--apply" in sys.argv:
    F.write_text(h, encoding="utf-8")
    print("written", len(orig), "->", len(h))
else:
    print("dry run ok", len(orig), "->", len(h))
