"""Teacher Notes for the AI Ready Wisconsin student course — one Markdown page per key.
Drafted 2026-10-28 from the course pages, the lab pages, the Playlab kit and the classroom-teacher panel review.
Anything in [square brackets] is a placeholder Ryan must fill; nothing in brackets is a fact."""

LABS = "https://uwo-ryan.github.io/titan-labs/"
PL = "https://www.playlab.ai/project/"

MODULES = {
    1: dict(name="AI: What It Is & What It Can Do", lab="Stump the Machine", labfile="m01-stump-the-machine.html", reel="What Can AI Actually Do?", app="T.I.T.A.N. – Prime", appid="cmtgeocui0tjcio0wmvdaik2i", disc="🏛️ The Fail Museum"),
    2: dict(name="AI as Your Learning Coach", lab="Teach-It-Back", labfile="m02-learning-coach.html", reel="Answer Machine or Learning Coach?", app="T.I.T.A.N. – Coach & Lil' T", appid="cmvr5ycnp0s5wi90wv9gm2u7e", disc="📓 Field Notes: Learning Coach"),
    3: dict(name="Getting Better Results from AI", lab="The Genie Problem", labfile="m03-genie-problem.html", reel="From Vague to Useful", app="T.I.T.A.N. – Genie Mode", appid="cmtgfpzqj0w3pio0wpb3ek4s0", disc="📓 Field Notes: The Genie Problem"),
    4: dict(name="Don't Believe Everything AI Tells You", lab="The Detective Agency", labfile="m04-detective-agency.html", reel="Sounds Right. Is It?", app="T.I.T.A.N. – Records Department", appid="cmvr62kdl0szpi90w5b9vjb8x", disc="📓 Field Notes: Detective Agency"),
    5: dict(name="Create with AI", lab="The Creative Gauntlet", labfile="m05-creative-gauntlet.html", reel="Generating Isn't Creating", app="T.I.T.A.N. – Creative Director", appid="cmvr64o4i0tixjn0w52j5iwxd", disc="🖼️ The Gallery"),
    6: dict(name="AI and Your Future", lab="The Career Time Machine", labfile="m06-career-time-machine.html", reel="Inside a Job", app="T.I.T.A.N. – Time Machine", appid="cmvr680vp0txii90w4okhqidr", disc="📓 Field Notes: Career Time Machine"),
    7: dict(name="Should I Use AI for This?", lab="You Be the Judge", labfile="m07-you-be-the-judge.html", reel="Can vs. Should", app="T.I.T.A.N. – Devil's Advocate", appid="cmvr68hli0vc7lk0wu2pm44jq", disc="📓 Field Notes: You Be the Judge"),
    8: dict(name="AI Challenge: Put It All Together", lab="The Titan Games", labfile="m08-titan-games.html", reel="Start to Finish", app="T.I.T.A.N. – The Examiner", appid="cmvr68sm10u3ai90w0s3kw3mh", disc="🏆 The Showcase"),
}

TITLES = {0: "Teacher Notes: Read Me First"} | {n: f"Teacher Notes: Module {n:02d}" for n in MODULES}


def links(n):
    m = MODULES[n]
    out = [f"- Explore page (the demo reel): [{m['reel']}]({LABS}m{n:02d}-explore-see-it-in-action.html)",
           f"- Lab page: [{m['lab']}]({LABS}{m['labfile']})",
           f"- The lab's AI, open in its own tab: [{m['app']}]({PL}{m['appid']}) (no account; this is the same link the lab's button opens)"]
    if n == 4:
        out.insert(1, "- The investigation tool: [The Scholar's Guide to Explainable AI](https://xai.mostlyharmlessscholar.com/) · how it works: [the guide page](https://www.mostlyharmlessscholar.com/the-scholars-guide-to-explainable-ai/)")
    return "\n".join(out)


FOOT = "\n\nCourse-wide setup (network, Playlab, codes, devices, discussions, the parent note) is on **Teacher Notes: Read Me First** at the top of Module 01. Keep this page unpublished; students never see unpublished items."

PAGES = {}

PAGES[0] = """
These notes are for the teacher running **IS002: AI for Wisconsin High School Students**. Each module also has its own Teacher Notes page at the top of the module. Everything here is unpublished, so students never see it.

**Before the first class:** open Module 01's lab on a student Chromebook, on the school network, signed in as a student would be. Confirm the chat loads inside the page and that T.I.T.A.N. answers. If either fails, nothing else in this course works yet; see "Network" below. Then send the parent note and collect permission; see "Permission and the parent note."

## How the course works

- Every module has the same eight items: Start Here, Learn, Explore, Do (the AI Lab), a discussion, a practice quiz, Wrap-Up, Resources. Start Here lists the module's objectives in student language.
- **Explore** pages are predict-then-reveal reels of real, unedited chats with the course's AI. Students guess what the AI will do, then see it. Nothing to set up.
- **Do** pages embed a lab from the course's lab site. Each lab is a themed set of mission cards. Students copy a mission line into the chat, do the work, and bring back a **code** that stamps their "AI Operator's License" on the page. Some cards stamp when the student files their written answers instead.
- **T.I.T.A.N.** is the course's AI assistant. It runs on Playlab, an AI platform built for schools. Students do not create accounts or sign in; the chat is embedded in the lab page, with a button to open it in its own tab. Every lab repeats the one rule that does not bend: no personal information in the chat, ever. Invented details are fine. No account does not mean no permission: Playlab's own terms require a parent's or guardian's permission for users under 18.
- Students do **not** need ChatGPT, Gemini, Copilot or any paid tool. Those appear only on the optional Resources pages, which say so.
- The discussions are where the work becomes visible. Every lab ends with a **Copy my Field Notes** button that formats the student's answers for the module's discussion. Treat the Field Notes post as the deliverable; stamps are motivation, not a grade.

## Network: what the district filter must allow

| Domain | Used by |
|---|---|
| uwo-ryan.github.io | every Explore page and every lab (embedded in Canvas) |
| www.playlab.ai (and playlab.ai) | T.I.T.A.N. chats inside every lab |
| xai.mostlyharmlessscholar.com | Module 04's email-investigation tool |
| doi.org and scholar.google.com | Module 04's citation check |
| bls.gov, onetonline.org, mynextmove.org, dwd.wisconsin.gov | Module 06's fact-check |
| express.adobe.com or canva.com (whichever your school provides) | Module 05's image making |
| uwosh.instructure.com | the Learn-page videos (students are already in Canvas) |

Test the embedded chat specifically: some filters allow a page but block the iframe inside it.

## Codes and stamps

- When a mission is done, T.I.T.A.N. ends its reply with one line in this form: `🔑 CODE: WORD — enter it on your lab page.` The student types the word into the CODE box on that card and presses **Stamp it**. One code per card; a card never needs a second one.
- T.I.T.A.N. is instructed to refuse to give or hint at a code until the step is really done, and to say so ("Codes are earned"). That refusal is working as designed.
- **If a code never comes** after a student clearly finished the step: have them send `What is my code for this round?` If they skipped the mission line (every card has a copy button), they must paste it; the chat does not know which game it is playing otherwise. Reloading the lab page starts a fresh chat, so copy anything worth keeping first.
- **If it still never comes**, the student pastes their Field Notes into the discussion anyway. The stamp is not required for credit, and the license page in Module 08 has checkboxes for "modules completed elsewhere."
- Do not read codes aloud or post them; the labs stop working as motivation the moment the class has the list. The key is in the box at the bottom of this page, for your eyes.

## Devices and saved work

- Stamps and Field Notes are saved **in the browser on that device**, not in Canvas. The lab inside Canvas and the lab opened in a new tab are two separate saves. A shared or wiped Chromebook loses them.
- So: same Chromebook, opened the same way, every time; and **Copy my Field Notes** into the discussion before the bell as the permanent record. Say this out loud in Module 01.
- Phones work for the Explore reels and in a pinch for labs ("On a phone?" link above each embed), but typing missions on a phone is slow. Plan on Chromebooks.

## Canvas settings worth changing

- All eight discussions are threaded, ungraded, and allow attachments (needed for The Gallery and The Showcase). They do **not** require a post before seeing replies; turn that on if you want original Field Notes rather than thirty echoes of the first post.
- Replies ("reply to a classmate who…") cannot happen in the same period people are posting. Make replies the next day's bell work.
- Every module is unpublished until you publish it. Publish one module at a time; the course is designed in order.

## Pacing: plan two periods per module

The pages' own estimates add up to 36–48 minutes per module before the discussion, the quiz, the cart and the logins. Our planning estimate for a 50-minute period with a mixed-readiness class:

| Module | Periods | Where the time goes |
|---|---|---|
| 01 Stump the Machine | 2 | the Fail Hunt; verifying one claim takes longer than the card says |
| 02 Teach-It-Back | 2 | the tutoring session with its mini-quiz; Lil' T is slow for English learners |
| 03 The Genie Problem | 2, tight | five stages, each needing two or three rebuilt wishes |
| 04 The Detective Agency | 2 | three cases in an outside tool, then DOI and Scholar lookups |
| 05 The Creative Gauntlet | 3, or 2 plus image-making at home | signing into the image tool, three generations, screenshots, upload |
| 06 The Career Time Machine | 2 | two role-played shifts; the fact-check needs 15 minutes, not 6 |
| 07 You Be the Judge | 2 | nine cases with reveals, then the Devil's Advocate |
| 08 The Titan Games | 3 to 4 | the build itself, the Examiner, the Showcase |

Day 1: Start Here, Learn, Explore, start the lab. Day 2: finish the lab, post Field Notes, practice quiz, Wrap-Up. The module pages give a minute-by-minute version.

## When the AI misbehaves

- T.I.T.A.N. is instructed to keep everything school-appropriate, to refuse personal information, to coach rather than do graded work, and to step out of the game and point a student in distress to a trusted adult. If a student reports any of those triggers, follow your school's normal process.
- Off-script, stuck, or stubborn: the student says what is not working ("that analogy lost me, try a sports one"). That is the skill the course teaches, so let them try first. Then: re-paste the mission line; then reload for a fresh chat.
- Anything that looks like a real failure (a code that never comes after a real attempt, a chat that refuses to play, an embed that will not load) is worth a note to the course team: what the student pasted, what came back, which lab. Send it to Ryan Van Scyoc, vanscyocr@uwosh.edu.
- The Fail Museum in Module 01 exists so that "the AI was confidently wrong" is a trophy, not a problem. Say so.

## Permission and the parent note

Playlab's own rules decide what goes home. Its [Terms of Use](https://www.playlab.ai/policies/terms-of-use) (updated March 18, 2026) and [Privacy Policy](https://www.playlab.ai/policies/privacy) (updated January 20, 2025) say:

- Playlab is not for children under 13. Users from 13 to 17 need a parent's or guardian's permission to use it.
- When students use it for school, the school or teacher is responsible for giving families notice and collecting any consent required (Terms, "School Use").
- Playlab does not sell personal information or show ads, and uses student data only for educational purposes at the direction of an educator, school or parent. It may use de-identified, aggregated data for research and to train educational AI models.
- Families can ask Playlab to delete personal information by emailing dsar@playlab.ai.

So before Module 01: send the note below and collect permission the way your district handles any approved online tool. If your district keeps an approved-tools list or signs data privacy agreements, check whether Playlab is on it. A student without permission can still do every lab's written cards and the discussions; pair them with a classmate's screen for the chat, with no typing of their own.

> AI Ready Wisconsin uses a course-built AI assistant called T.I.T.A.N., which runs on Playlab, an AI platform built for education. Students do not create accounts or sign in, and every lab tells them never to enter personal information such as full names, school names or private details; invented details are fine. Playlab does not sell personal information or show ads; it may use de-identified, combined data for research and to improve educational AI. Playlab asks that students under 18 have a parent's or guardian's permission to use it, so please [your school's permission step: sign and return the form, or reply to this message]. Nothing students type to the AI is graded; the work the class sees is the Field Notes each student chooses to post in Canvas. Module 4 also uses a public research demonstration that explains why a sample email looks suspicious; students paste in training emails supplied by the lab, never real messages. No paid subscription and no ChatGPT account are needed.

## Accessibility

Every lab and Explore page follows WCAG 2.1: keyboard navigation, visible focus, 3:1 field borders, a compact layout under 700 px. Reels move keyboard focus to each new answer. Practice quizzes shuffle answers and give feedback on every option. If a student needs the lab outside the iframe, the "Open the lab in a new tab" link above each embed is the fix.

## The code key (teacher only; never publish this page)

| Module | Card | Stamp |
|---|---|---|
| 01 | Two Truths and a Hallucination · Impress round · Fail Hunt · Debrief | FIBFINDER · SHOWOFF · GOTCHA · SCOREBOARD |
| 02 | Five Levels · Tutor session · Teach-back · Your session | TOPRUNG · AHAMOMENT · PROFESSOR · LIGHTBULB |
| 03 | Rub the lamp · Hole 1 · Hole 2 · Hole 3 · Final wish | BRASSLAMP · SANDSTORM · MAGICCARPET · THIRDWISH · FREEGENIE |
| 04 | Cases 1–3 · Fabrication Forensics | the cases stamp when filed · PAPERTRAIL |
| 05 | Basket · Director · Log · Credits | stamps when locked · ARTCRITIC · stamps when logged · stamps when signed |
| 06 | 2026 shift · 2036 shift · Fact-check · Compass | PUNCHCARD · FUTUREPROOF · RECEIPTS · stamps when set |
| 07 | Rulings · The Trial · My Rules | stamp as the dials are set · STEELMAN · stamps when signed |
| 08 | Quest · Build log · The Examiner | stamps when accepted · stamps when sealed · BOSSFIGHT |
"""

PAGES[1] = f"""
**Before this module**

- [ ] Open the lab on a student Chromebook on the school network; confirm the chat loads inside the page and answers.
- [ ] Decide where Field Notes go (the Fail Museum discussion is the default) and whether replies are Day 2 bell work.
- [ ] Say the device rule out loud: same Chromebook, same way, Copy my Field Notes before the bell.
- [ ] Permission is in for every student. Playlab's terms require a parent's or guardian's permission under 18; the parent note is on Read Me First.

**What this module is.** The big question is what AI actually is and how you know when to trust it. The through-line, which every later module leans on, is that AI sounds exactly as confident when it is wrong as when it is right. The lab, **Stump the Machine**, has students make T.I.T.A.N. impress them with something real, then hunt for an error with evidence. Every caught error is "+1 HUMAN."

**Two periods**

| Day 1 (50 min) | Day 2 (50 min) |
|---|---|
| Start Here 5 · Learn 10 · Explore reel 10 ("What Can AI Actually Do?": six demos, one trap; predict before each reveal) · lab warm-up and Impress round 20 | Fail Hunt 15 · Debrief 5 · Field Notes into the Fail Museum 10 · practice quiz 10 · Wrap-Up 5 · replies next day |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| Warm-up: Two Truths and a Hallucination (~4 min) | picks a topic they know; T.I.T.A.N. states three facts, one invented; student accuses | code after the reveal, right or wrong | the point is that tone tells you nothing; a wrong guess still earns the code |
| Round 1: Make it impress you (~5) | brings a real task, fills the mission template, must push back at least once | code after the improved version | "I'm a [grade] student" is the only self-description allowed; no names |
| Round 2: The Fail Hunt (~7, really 12) | pastes `M01 FAIL HUNT` (copy button), runs two probes, proves an error with evidence | code when they show a specific error and how they know | a vague "that's wrong" earns nothing; if T.I.T.A.N. holds up after real probes, documenting what they tried also earns it |
| Debrief: The uncomfortable question (~3) | answers "when AI sounds confident, what does that tell you?" | code after a thoughtful answer | one sentence is enough if it is their own |

**When T.I.T.A.N. misbehaves.** The most common stall is Round 2 without the mission line: the chat answers probes normally and never concedes. Have them paste `M01 FAIL HUNT` first. The second is a student who cannot find an error; the honest fallback is written into the game (document the probes, earn the code). Do not help them "trap" it with trick questions; the lesson is evidence, not gotchas.

**The discussion: The Fail Museum.** Good posts name what they asked, what the AI got wrong, and how they caught it. The reply prompt ("could you have caught their fail without knowing the topic?") is the one to push on Day 2: it is the course's first encounter with "I would have to check." With the student's OK, feature one or two exhibits, first name only.

**Watch for**

- Students who open ChatGPT out of habit. The course never needs it; the Resources page explains the account rules if they ask.
- English learners in Two Truths: the three claims arrive in the same register, which is the point, but let them pick a topic from home or a hobby so the vocabulary is theirs.
- "Stumping" with homework. Round 1 is for a real task, and T.I.T.A.N. is told to coach rather than do graded work. If a student tries to get an essay written, that is Module 07's conversation arriving early; name it and move on.

**Links**

{links(1)}
"""

PAGES[2] = f"""
**Before this module**

- [ ] Re-run the Chromebook check on this lab; it uses a different T.I.T.A.N. app (Coach & Lil' T) than Module 01.
- [ ] Ask students to bring one thing they are honestly stuck on, from any class. The lab is empty without it.

**What this module is.** Can AI help you learn something, not just hand you the answer? The lab, **Teach-It-Back**, puts T.I.T.A.N. in Coach Mode: it explains, quizzes and switches strategies but will not do the thinking. Then the twist: the student teaches the same idea to Lil' T, a hopelessly confused little-sibling model that repeats ideas back wrong until corrected. If they can survive Lil' T, they understand it.

**Two periods**

| Day 1 (50 min) | Day 2 (50 min) |
|---|---|
| Start Here 5 · Learn 10 (short video on the page) · Explore reel 10 ("Answer Machine or Learning Coach?": six chats; who is doing the learning?) · Five Levels warm-up 5 · start the tutoring session 15 | finish the tutoring session and mini-quiz 10 · Teach-back 12 · Your session 8 · Field Notes post 8 · practice quiz 8 · Wrap-Up 4 |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| Warm-up: The Five Levels (~3 min) | names any topic; the coach explains it five ways, little-kid to expert; student says which level fits | code when they name their level | the "one rung up" line is the hook for the whole module |
| Phase 1: The tutoring session (~7, really 12) | brings what they are stuck on and where they get lost; must make the coach switch strategies at least twice; ends with a three-question mini-quiz, one question at a time | code after the quiz, any score | students who settle for the first explanation; the checklist on the card (another way, analogy, example, ask me questions, quiz me, let me try one) is the menu |
| Phase 2: Teach it back to Lil' T (~6) | pastes `M02 TEACH-BACK`; Lil' T asks at least four questions and repeats the idea back wrong at least twice; student corrects it | code when Lil' T can state it correctly | this is slow for English learners; let them teach in their strongest register, the coach is told to allow one hint |
| Your turn: Design your own session (~4) | plans a second topic and strategies on the card, runs it, files `M02 APPLY REPORT` | code after the report | the report asks which strategy worked and why; that line is the Field Notes gold |

**When T.I.T.A.N. misbehaves.** "The coach keeps explaining the same way" is the module's own lesson: the student has to ask for a different strategy by name. If Lil' T never gets confused (it is instructed to), the student should send `M02 TEACH-BACK` again. A student who asks the coach to just give the answer will be refused; that is correct.

**The discussion: Field Notes: Learning Coach.** The prompt asks which strategy worked and where the line is between AI helping you learn and doing the learning. Thirty posts will say "the analogy." Ask for the one line the coach said that made it click; no two should quote the same line. The reply prompt pairs students whose strategies differed.

**Watch for**

- Homework topics are fine and encouraged; the coach will not write the assignment, it will teach the concept.
- The Start Here page mentions NotebookLM as "you'll see." The Explore reel is T.I.T.A.N. only; the source-grounded notebook idea appears on the optional Resources page. If a student asks, that is where it is.

**Links**

{links(2)}
"""

PAGES[3] = f"""
**Before this module**

- [ ] Chromebook check on this lab (Genie Mode is its own app and the chat is embedded in "the lamp").
- [ ] Skim the Learn page framework once: Goal, Context, Directions, Constraints, Evaluate, Refine. Every card grades a wish against it.

**What this module is.** Why does AI sometimes give you exactly what you need and other times something useless? The lab, **The Genie Problem**, traps T.I.T.A.N. in a lamp where it grants exactly what you ask for, pettily. Students rebuild deliberately terrible wishes until the genie has no loopholes left. Hole 3 has a twist: no new wishes, only follow-up instructions, because improving a result instead of starting over is the skill that separates good AI users from everyone else.

**Two periods (tight)**

| Day 1 (50 min) | Day 2 (50 min) |
|---|---|
| Start Here 5 · Learn 10 (short video on the page) · Explore reel 10 ("From Vague to Useful": one presentation, five rounds of asking better) · Rub the lamp 3 · Hole 1 12 · start Hole 2 | Hole 2 10 · Hole 3 12 · Final wish 8 · Field Notes post 8 · practice quiz 8 · Wrap-Up 4; if short on time, the Final wish can be homework |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| Warm-up: Rub the lamp (~2 min) | introduces themselves (no names) and makes one harmless test wish | code | "make me a sandwich" shows what literal looks like |
| Hole 1: The Study Wish, par 3 (~4) | starts from `help me study`, rebuilds with a real subject, level, form of help and one limit | code when the genie is satisfied | "par 3" means about three tries; the +/− counter is theirs to click |
| Hole 2: The Project Wish, par 3 (~4) | starts from `give me ideas for my project`; must name an exact number, a format and two real limits | code | the genie buries vague wishes in useless ideas on purpose |
| Hole 3: The Polishing Wish, par 4 (~5) | starts from `write something about Wisconsin`, then may only give follow-up instructions, at least two rounds | code | first-timers try to start over; the card forbids it; "evaluate, then tell it what to change" |
| Final wish: Free the genie (~4) | one real wish with all four elements, refined at least once | code; the genie tells them what they got good at | the best Field Notes come from here |

**When T.I.T.A.N. misbehaves.** The genie is supposed to be difficult. After three tries on a hole it starts offering hints, and the student may ask for one. A student whose wish is genuinely good and still gets no code should ask what is missing; the genie judges the build, not the subject. If the chat loses the thread, reloading starts a fresh genie; the student restarts the hole with its copy button.

**The discussion: Field Notes: The Genie Problem.** The prompt asks which single change made the biggest difference and tells repliers to steal a classmate's best move. That reply is the module's best assessment; make it Day 2 bell work.

**Watch for**

- Golf words: "par," "hole." The card now glosses them; a one-sentence explanation on Day 1 saves questions.
- The Start Here page says students will "see what happens when the same request is given to another AI system such as Gemini or Copilot." That comparison lives on the optional Resources page, not in the reel.

**Links**

{links(3)}
"""

PAGES[4] = f"""
**Before this module**

- [ ] Open the investigation tool on a student Chromebook: [xai.mostlyharmlessscholar.com](https://xai.mostlyharmlessscholar.com/). Paste any of the lab's training emails, try all three explanation methods, press **Analyze Email**. The natural-language method takes about ten seconds.
- [ ] Confirm doi.org and scholar.google.com open on the school network; the final case needs both.
- [ ] Read the one-page guide to the tool, [The Scholar's Guide to Explainable AI](https://www.mostlyharmlessscholar.com/the-scholars-guide-to-explainable-ai/), so you can answer "is the heatmap real?" (it is a simulated illustration, and the tool says so).

**What this module is.** AI gives you an answer in seconds; how do you know it is true? The lab, **The Detective Agency**, promotes the student to Senior Detective. Three AI "junior detectives" examine suspicious emails, each explaining its conclusion a different way: Reggie Rules (a rule list), Vera Verbose (a paragraph from a language model) and Heatmap Hank (highlighted words). Then, in the basement, T.I.T.A.N.'s Records Department hands over three perfect-looking citations for any claim, at least one fabricated, and the student has to find out which without asking the clerk. The question of the day: does understanding **why** an AI decided something prove it is right?

**The tool, in one minute.** It is a public research demonstration, not a security product, and it says so on screen. The student pastes an email into the box, picks one of three explanation methods, and presses Analyze Email: the rule list is Reggie, the paragraph is Vera, the highlighted words are Hank. The tool has no built-in email list, so the lab page now supplies four fictional **training cases** with copy buttons (an account-deactivation scam, a legitimate band-trip reminder, a gift-card "favor" from the principal, a scholarship that asks for a Social Security number). Students never paste real emails; the lab says so in bold.

What the detectives do with them, from our test run on 2026-10-28:

- Case A (account deactivation): all three agree. Reggie flags account terms, urgent language and a link; Vera writes six numbered concerns; Hank lights up URGENT, account, verify.
- Case B (band trip, legitimate): Reggie flags only "a hyperlink is present." Vera says everything could be legitimate and tells you how to verify. The detectives are uneven, which is Case 2's job.
- Case C (gift cards, no link): Reggie finds **nothing**. Vera finds seven red flags. The rulebook is confidently silent.
- Case D (scholarship asking for an SSN): Reggie again finds nothing. A dangerous email with no rule hits is the cleanest "explanation is not proof" case there is.

**Two periods**

| Day 1 (50 min) | Day 2 (50 min) |
|---|---|
| Start Here 5 · Learn 10 (short video on the page) · Explore reel 10 ("Sounds Right. Is It?": five real questions; check even the right answers) · tool orientation 5 · Case 1 10 · start Case 2 | Case 2 8 · Case 3 8 · Fabrication Forensics 15 · Field Notes post 8 · practice quiz 8 · Wrap-Up 3 |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| Case 1: The warm-up case (~4 min) | runs Case A through all three detectives, records the evidence, makes a call | stamps when filed, no code | students who run one method and stop; all three, every case |
| Case 2: When the detectives disagree (~4) | runs Case B or C, writes where the explanations pulled apart and what broke the tie | stamps when filed | "Vera sounded sure" is not evidence; push for what she pointed at |
| Case 3: Explanation ≠ proof (~4) | runs Case D or any case; answers "if the AI were wrong, how would you find out outside the tool?" | stamps when filed | the answer should name something outside the tool: the real sender address, calling the office, the school's own site |
| Final case: Fabrication Forensics (~6, really 12) | sends `RECORDS REQUEST: [a claim]`, gets three citations, checks each title on Google Scholar and each DOI at doi.org, files `VERIFICATION REPORT` | PAPERTRAIL when the report has specific findings for all three | the clerk refuses to say which are real ("the archive does not audit itself"); that refusal is the lesson, not a malfunction |

**When T.I.T.A.N. misbehaves.** The Records Department will not confirm or deny a citation; students must search. A vague report ("I couldn't find it") gets sent back by design; the report needs what they searched and what came back. If the tool's natural-language method is slow or errors, the rule and heatmap methods still work and the case can be filed on those two.

**The discussion: Field Notes: Detective Agency.** The prompt asks which detective they trusted most and whether understanding why proves the AI is right. The reply pairs students who trusted different detectives; that disagreement is the module.

**Watch for**

- Phishing is personal for some families. Keep the cases on the fictional training emails and steer students who want to analyze "the email my mom got" to the Resources page's STOP, SPOT, CHECK, DECIDE habit instead.
- The tool is Steve Schilhabel's research demonstration (UW Oshkosh), published as The Scholar's Guide to Explainable AI on his site, The Mostly Harmless Scholar. That is what the lab's "built at UW Oshkosh" caption refers to.

**Links**

{links(4)}
"""

PAGES[5] = f"""
**Before this module, two weeks ahead**

- [ ] Confirm **one image tool** students can sign into on school Chromebooks with school accounts: Adobe Express for Education or Canva for Education are the lab's buttons; Microsoft Designer with school accounts also works. Students must not create personal accounts for this.
- [ ] Confirm attachments work in the Gallery discussion (course setting is on) and that students know how to screenshot on a Chromebook (Ctrl+Shift+Show windows).
- [ ] Decide the no-tool fallback is acceptable: describe the image in words to the Creative Director and sketch on paper. The rounds and the credits still count. The lab offers this fallback itself.

**What this module is.** If AI helps create something, whose creativity is it? The lab, **The Creative Gauntlet**, runs on cooking-show rules: a mystery basket assigns a format, a subject and one ridiculous twist. The student generates an image in the school's tool, then reports to T.I.T.A.N.'s Creative Director (beret, opinions) for two critiques and a challenge, three rounds minimum, logging what changed each round and finally rolling honest credits: what came from me, what AI contributed, what I overruled. Generating is the beginning of creating, not the end.

**Three periods, or two plus image-making at home (equity risk: not every home has the tool)**

| Day 1 (50 min) | Day 2 (50 min) | Day 3 (50 min) |
|---|---|---|
| Start Here 5 · Learn 10 (short video on the page) · Explore reel 10 ("Generating Isn't Creating": one slogan, five rounds) · spin and lock the basket 5 · sign in to the image tool and generate Round 1 20 | Critique Round 1 and generate Round 2 15 · Round 2 critique and generate Round 3 15 · Round 3 critique 8 · The Log 8 · start Credits | Roll Credits 8 · Gallery post with before/after images 15 · practice quiz 8 · Wrap-Up 4 · replies 10 |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| Step 1: Spin the mystery basket | spins, then locks; re-spinning forever is "a violation of cooking-show law" | stamps when locked | students fishing for an easy basket; one or two spins, then lock |
| Step 2: Create it | writes a prompt from the basket in the image tool; saves or screenshots every version | no stamp | Module 03 skills apply: specific creative direction lands closer |
| Step 3: Three rounds with the Director (~10 min, really 30 across the periods) | after each generation, pastes `CRITIQUE ROUND n` with the basket, an honest description and the prompt; gets two critiques and one challenge; may overrule a note with a reason | ARTCRITIC after three completed rounds | the Director cannot see the image; thin descriptions get sent back to look harder, which is the point |
| The Log (~3) | what changed Round 1→2 and 2→3, and what they kept on purpose | stamps when logged | "I kept it because it's my favorite part" is a valid creative decision |
| Roll Credits (~3) | idea from me, what AI did, what I overruled, does it feel like mine | stamps when signed | this is the module's assessment; read these |

**When the AI misbehaves.** Two different AIs are in play. If the **image tool** produces something weird or inappropriate, the lab's rule is: do not share it, change the prompt, tell the instructor if it keeps happening. If the **Director** gives generic notes, the student's description was generic; have them name colors, composition, what the twist looks like. If it refuses to critique without a description, that is by design.

**The discussion: The Gallery.** Attach the final image (or link it) plus the Field Notes with the credits. Before/after pairs from Round 1 to Round 3 are the best posts and the easiest to praise. The reply prompt asks for a creative decision the classmate made that AI did not.

**Watch for**

- School-appropriate prompts, both directions: what they ask the image tool for, and what comes back. The lab states both rules in bold.
- Free tiers cap generations; three rounds is the minimum and is usually enough.
- Students without the tool at home must not be the ones doing it at home; if Day 3 is impossible, drop replies, not Credits.

**Links**

{links(5)}
"""

PAGES[6] = f"""
**Before this module**

- [ ] Chromebook check on this lab (the Time Machine is its own app).
- [ ] Open the three fact-check sources on the school network: the [BLS Occupational Outlook Handbook](https://www.bls.gov/ooh/), [O*NET OnLine](https://www.onetonline.org/) and the Wisconsin DWD link on the lab page. The Resources page also lists [My Next Move](https://www.mynextmove.org/).
- [ ] Budget 15 minutes for the fact-check, not the card's 6.

**What this module is.** How might AI change your future, and how do you prepare for one still being invented? The lab, **The Career Time Machine**, interviews the student about interests and strengths (never name, school or town), proposes three careers including one they have never heard of, and drops them into a day on the job in 2026 with decision points: hand this task to AI, or keep it human? Then the lever: the same job in 2036. Along the way the machine states "facts" about pay, education and outlook marked with 📌, generated like everything else; the student's last mission is finding out which are true.

**Two periods**

| Day 1 (50 min) | Day 2 (50 min) |
|---|---|
| Start Here 5 · Learn 10 · Explore reel 8 ("Inside a Job": one career, four questions; check what it claims) · 2026 shift 15 · jot the 📌 claims in the tracker · start the 2036 shift | 2036 shift 12 · fact-check 15 · compass 3 · Field Notes post 8 · practice quiz 8 · Wrap-Up 4 |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| Shift 1: A day on the job, 2026 (~6 min, really 12) | pastes `TIME MACHINE START`, answers three or four interview questions, picks a career, works three or four decision points | PUNCHCARD when the shift ends | the unfamiliar career is usually the most interesting; nudge toward it |
| Shift 2: Same job, 2036 (~6) | pastes `PULL THE LEVER`; notes what vanished (automation), what changed (augmentation), which human choices mattered more | FUTUREPROOF | the last question, "what did you still do that no AI did," feeds the Field Notes |
| The Hunt: Fact-check the machine (~6, really 15) | pastes `SHOW ME THE CLAIMS`; checks three 📌 claims against OOH, O*NET or DWD; fills the tracker; files `FACTCHECK REPORT` with the source and what it said | RECEIPTS when three claims are checked against named sources | "couldn't confirm" on all three means they asked the machine instead of a source; start with the OOH, search the job title, read Pay and Job Outlook |
| Your turn: Point your compass (~2) | one pathway to investigate for real, and the first question a real source should answer | stamps when set | the Resources page is where that investigation continues |

**When T.I.T.A.N. misbehaves.** The machine is told never to say whether a claim was right and never to tell a student which career to choose; both refusals are correct. If it forgets the 📌 marks, the student asks it to list its claims again with the pins. If it asks for a name, school or town, the student declines; interests only.

**The discussion: Field Notes: Career Time Machine.** The prompt asks which claims held up and what the 2036 version of them did that no AI did. Ask students to lead with the claim that was wrong and the source that proved it. The reply pairs students with a classmate who explored a career they have never considered.

**Watch for**

- Privacy is the sharpest here: the lab says "share your interests, not your identity." The Start Here page's "What you'll do" list repeats it.
- Pay and outlook numbers from the machine are plausible and sometimes wrong, which is the lesson. Do not correct them yourself; let the sources do it.

**Links**

{links(6)}
"""

PAGES[7] = f"""
**Before this module**

- [ ] Know your own classroom and school AI rules; the lab says they always outrank a lab verdict, and the Devil's Advocate argues from "class and school rules come first."
- [ ] Read the Start Here page's paragraph on the book *If Anyone Builds It, Everyone Dies*. The course does not assign the book; the Learn page mentions the larger debate briefly. The title alone may draw a parent question; the answer is that students read one neutral paragraph and are asked what they think.

**What this module is.** Just because AI can do something, should you use it? No new tool; the tool is the student's judgment. The lab, **You Be the Judge**, puts nine situations on a docket (the list of cases). For each, the student sets a dial, Use it, It depends, Don't use it, then sees what was worth weighing. Then they take their hardest call to T.I.T.A.N.'s Devil's Advocate, which argues the other side harder than anyone they know. Changing your mind for a better argument counts as winning; holding firm with good reasons counts too. They finish by writing their personal AI rules.

**Two periods**

| Day 1 (50 min) | Day 2 (50 min) |
|---|---|
| Start Here 5 · Learn 10 · Explore reel 8 ("Can vs. Should": four requests AI can help with; should it?) · the docket, nine cases with reveals 20 · pick the hardest call | The Trial 12 · My Rules 8 · Field Notes post with rules 8 · practice quiz 8 · Wrap-Up 4 · replies 8 |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| The docket: nine cases (~12 min) | rules on each case, reads the considerations and how others called it | rulings stamp as the dials are set | the "how others called it" bars are the design team's prediction, not class data; say so if asked |
| The Trial: Defend your hardest call (~6) | pastes `DEBATE:` with the scenario, their ruling and their reasoning; rebuts at least three rounds | STEELMAN after the Advocate judges the reasoning | "it depends" is allowed only if they say what it depends on; the Advocate will insist |
| Your turn: Write your personal AI rules (~4) | I will, I won't, I'll always double-check when, I'll tell people when | stamps when signed | short and honest beats long and impressive; these are worth keeping all year |

**When T.I.T.A.N. misbehaves.** The Advocate is supposed to disagree with whatever the student said; a student who finds it "unfair" has met the exercise. It judges reasoning, not the ruling, so a student may keep their verdict and still earn the code. Scenarios stay hypothetical; if a student brings a real situation where someone is being hurt or unsafe, the Advocate steps out and points them to a trusted adult, and so should you.

**The discussion: Field Notes: You Be the Judge.** Rules included. The prompt asks which case was the hardest call and whether anything changed their ruling. The reply pairs students who ruled differently on the same case and asks where the reasoning actually splits; that is the module's assessment.

**Watch for**

- Academic-integrity cases will produce "but you let us use it for…" conversations. Good. Your actual rules are the tiebreaker, and the lab says so.
- Students sharing real personal stories in the chat; the house rule is hypotheticals only.

**Links**

{links(7)}
"""

PAGES[8] = f"""
**Before this module**

- [ ] Plan three to four periods, and decide what "done enough to defend" means for your class; the Examiner accepts a project that is done enough.
- [ ] Confirm attachments work in the Showcase discussion and that students can save their project somewhere they can link or attach it.
- [ ] Remind students of the device rule: the complete license page assembles all eight modules from stamps saved on **this** device and has checkboxes for modules completed elsewhere.

**What this module is.** Can you decide when, why and how to use AI without someone telling you what to do? Nobody tells the student what to type. The lab, **The Titan Games**, has them choose a quest from eight pathways (learn something hard, create something, investigate, plan, solve, communicate, explore a future, their own idea), answer three questions before opening any AI tool (what am I trying to accomplish; should AI be part of this; which tools and why), build it with any approved tools, keep a log of at least three moments, and then face The Examiner, T.I.T.A.N.'s final form, which asks five questions one at a time and sends vague answers back. "No, not for that part" is a passing answer, and might be the best one.

**Three to four periods**

| Day 1 (50 min) | Day 2 (50 min) | Day 3 (50 min) | Day 4 (if needed) |
|---|---|---|---|
| Start Here 5 · Learn briefing 7 · Explore reel 10 ("Start to Finish": one real project, six decisions) · choose and accept the quest 15 · start the build | build and log 50 | finish the build 20 · seal the log 5 · face the Examiner 15 · copy Capstone Notes 5 | Showcase post with the project 20 · celebrate two classmates' projects 15 · practice quiz 8 · Wrap-Up 5 |

**The lab, card by card**

| Card | What the student does | Stamp | Watch for |
|---|---|---|---|
| Step 1: Choose your quest (~5 min) | picks a pathway, answers the three questions in writing | stamps when accepted | "should AI be part of this?" answered with "no, not for that part" is strong; do not talk them out of it |
| Step 2: Build it and keep the log | does the work with approved tools; three log entries: what I did, what AI did, what I decided; one must be a refinement, rejection or verification; one must be a decision entirely theirs | stamps when sealed | students who log at the end from memory; the log is the ammunition for the Examiner, so it should be written during the build |
| Step 3: Face the Examiner (~8, really 12) | pastes `EXAMINATION START:` with the goal, what they made and which tools (and where they chose not to); answers five questions one at a time | BOSSFIGHT after five real answers and the verdict | vague answers get one follow-up each; that is the design |

**When T.I.T.A.N. misbehaves.** The Examiner asks one question at a time and waits; students who paste all five answers at once will be asked again one by one. It is told to name their strongest moment and one skill to keep building; if the verdict is missing, the student asks for it. Any other T.I.T.A.N. app may be used during the build (the Coach for learning, the Director for images, the Records Department for sources); the links are on each module's Teacher Notes page.

**The discussion: The Showcase.** The one everyone reads. Post the Capstone Notes (the lab's copy button) and the project, attached, linked or described: what they chose, where AI belonged and where it did not, what they verified, what the Examiner ruled. Then specific praise for two classmates' projects. If you grade anything in this course, grade this post against the log.

**Watch for**

- The whole-season license is a motivator, not a record. Students who lost stamps on another device tick the "completed elsewhere" boxes; their Field Notes posts are the record.
- Module 07 rides along: a quest that involves other people's information or feelings needs the same judgment, and the lab says so in the standing rules.
- The Wrap-Up ends the course. There is no certificate in the student course; if your school issues one, that is yours to add.

**Links**

{links(8)}
"""

for n in MODULES:
    PAGES[n] = PAGES[n].strip() + FOOT
PAGES[0] = PAGES[0].strip()
