"""Build the student Explore pages (titan-labs/mNN-explore-see-it-in-action.html) and the educator
demo blocks (Canvas HTML) from page specs in _explore/pages/ and real transcripts in _explore/captures/.

    uv run --with pyyaml python _explore/build.py            # every spec
    uv run --with pyyaml python _explore/build.py s-m02      # one

Student pages reuse M01's stylesheet and player (m01-explore-see-it-in-action.html is the template and
is never rewritten). A scene may show earlier turns of the same chat ("thread") before the prompt.
Educator specs produce _explore/out/<page>.canvas.html: inline-styled blocks for the Canvas page body.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATE = ROOT / "m01-explore-see-it-in-action.html"
OUT = HERE / "out"
SITE = "https://uwo-ryan.github.io/titan-labs/"


def turns(page: str) -> dict[str, list[dict]]:
    d = json.loads((HERE / "captures" / f"{page}.json").read_text(encoding="utf-8"))
    return {s["id"]: s["turns"] for s in d["sessions"]}, {s["id"]: s for s in d["sessions"]}


def tidy(h: str) -> str:
    """Captured HTML as the page shows it: line breaks inside a paragraph become <br>."""
    def br(m):
        return m.group(1) + m.group(2).strip().replace("\n", "<br>") + m.group(3)
    h = re.sub(r"(<p[^>]*>)([\s\S]*?)(</p>)", br, h)
    h = h.replace("Copy table<table>", "<table>")            # Playlab's copy-button label, not the AI's words

    def math(m):   # TeX left in captured math: subscripts, and the arrow early captures lost to a double space
        t = re.sub(r"(\S) {2,}(\S)", r"\1 → \2", m.group(2))
        t = re.sub(r"_(\d+)", r"<sub>\1</sub>", t)
        t = re.sub(r"\^(\d+)", r"<sup>\1</sup>", t)
        return m.group(1) + t + m.group(3)
    h = re.sub(r'(<(?:span|p) class="math">)([\s\S]*?)(</(?:span|p)>)', math, h)
    return h.strip()


def ref(sess: dict, r: str) -> dict:
    """'B3' → session B, turn 3 (0-based, counting from the first prompt)."""
    m = re.fullmatch(r"([A-Z])(\d+)", r)
    return sess[m[1]][int(m[2])]


# ---------------------------------------------------------------- student pages (interactive)

EXTRA_CSS = """
  .bubble .math { font-family: Consolas, Monaco, monospace; }
  .bubble.ai hr { border: 0; border-top: 1px solid #333333; margin: 12px 0; }
  .bubble.ai ul, .bubble.ai ol { margin: 0 0 10px; padding-left: 22px; }
  .bubble.ai li { margin: 0 0 6px; line-height: 1.55; }
  .bubble.ai li p { margin: 0 0 6px; }
  .bubble.ai table { border-collapse: collapse; margin: 0 0 10px; font-size: 14px; }
  .bubble.ai th, .bubble.ai td { border: 1px solid #444444; padding: 6px 8px; text-align: left; vertical-align: top; }
  .earlier { border-left: 3px solid #e0e0e0; padding-left: 12px; margin: 0 0 16px; }
  .earlier .label { font-size: 12px; font-weight: bold; letter-spacing: .06em; color: #555555; margin: 0 0 8px; }
  .earlier .bubble { opacity: .78; font-size: 14px; }
  .earlier .bubble.ai p { font-size: 14px; }
"""

PLAYER_JS = r"""
<script>
(function () {
  "use strict";
  var SCENES = %SCENES%;
  var idx = 0, revealed = {}, picked = {};
  var dots = document.getElementById("dots");
  SCENES.forEach(function (_, i) {
    var d = document.createElement("button");
    d.className = "dot"; d.type = "button";
    d.setAttribute("aria-label", "Go to scene " + (i + 1));
    d.addEventListener("click", function () { idx = i; render(); });
    dots.appendChild(d);
  });
  function bubble(who, html) {
    var b = document.createElement("div");
    b.className = "bubble " + who;
    b.innerHTML = (who === "you" ? '<span class="who">YOU ASK</span>' : '<span class="who">🤖 T.I.T.A.N. — REAL RESPONSE</span>') + html;
    return b;
  }
  function render() {
    var s = SCENES[idx];
    document.getElementById("sceneTag").textContent = s.tag;
    document.getElementById("sceneTitle").textContent = s.title;
    Array.prototype.forEach.call(dots.children, function (d, i) {
      d.className = "dot" + (i < idx || revealed[i] ? " on" : "") + (i === idx ? " now" : "");
      if (i === idx) d.setAttribute("aria-current", "step"); else d.removeAttribute("aria-current");
    });
    var body = document.getElementById("sceneBody");
    body.innerHTML = "";
    if (s.thread && s.thread.length) {
      var e = document.createElement("div"); e.className = "earlier";
      e.innerHTML = '<p class="label">EARLIER IN THIS CHAT</p>';
      s.thread.forEach(function (t) { e.appendChild(bubble(t.who, t.html)); });
      body.appendChild(e);
    }
    body.appendChild(bubble("you", s.prompt));
    if (!revealed[idx]) {
      var pr = document.createElement("div");
      pr.className = "predict";
      pr.innerHTML = "<h4>🔮 Before it answers — your prediction: " + s.predict + "</h4>";
      var opts = document.createElement("div"); opts.className = "opts";
      s.opts.forEach(function (o, j) {
        var b = document.createElement("button"); b.type = "button"; b.textContent = String.fromCharCode(65 + j) + ") " + o;
        b.addEventListener("click", function () { picked[idx] = j; revealed[idx] = true; render(); });
        opts.appendChild(b);
      });
      pr.appendChild(opts);
      body.appendChild(pr);
    } else {
      if (picked[idx] !== undefined) {
        var chosen = document.createElement("div");
        chosen.className = "predict";
        chosen.innerHTML = "<h4>🔮 You predicted: <em>" + s.opts[picked[idx]] + "</em></h4>";
        body.appendChild(chosen);
      }
      var ai = bubble("ai", s.ai); ai.className += " reveal-in"; body.appendChild(ai);
      var no = document.createElement("div");
      no.className = "notice reveal-in";
      no.innerHTML = "<h4>👁️ WHAT TO NOTICE</h4>" + s.notice;
      body.appendChild(no);
    }
    document.getElementById("prevBtn").disabled = idx === 0;
    var next = document.getElementById("nextBtn");
    if (idx === SCENES.length - 1) { next.textContent = revealed[idx] ? "🎬 That's the reel — scroll on ↓" : "Reveal first ↑"; next.disabled = true; }
    else { next.textContent = "Next scene →"; next.disabled = !revealed[idx]; }
    if (window.innerWidth < 700) document.getElementById("player").scrollIntoView({ block: "start" });
  }
  document.getElementById("prevBtn").addEventListener("click", function () { if (idx > 0) { idx--; render(); } });
  document.getElementById("nextBtn").addEventListener("click", function () { if (idx < SCENES.length - 1 && revealed[idx]) { idx++; render(); } });
  render();
})();
</script>
"""


def paras(items) -> str:
    return "\n".join(f"      <p>{p}</p>" for p in items)


def build_student(name: str, spec: dict) -> Path:
    sess, meta = turns(name)
    tpl = TEMPLATE.read_text(encoding="utf-8")
    css = tpl[tpl.index("<style>") + 7: tpl.index("</style>")]
    scenes = []
    for sc in spec["scenes"]:
        p, a = ref(sess, sc["prompt"]), ref(sess, sc["ai"])
        assert p["who"] == "you" and a["who"] == "ai", sc["tag"]
        scenes.append({
            "tag": sc["tag"], "title": sc["title"],
            "thread": [{"who": ref(sess, r)["who"], "html": tidy(ref(sess, r)["html"])} for r in sc.get("thread", [])],
            "prompt": tidy(p["html"]), "predict": sc["predict"], "opts": sc["opts"],
            "ai": tidy(a["html"]), "notice": "".join(f"<p>{x}</p>" for x in sc["notice"]),
        })
    used = sorted({r[0] for sc in spec["scenes"] for r in [sc["prompt"], sc["ai"], *sc.get("thread", [])]})
    captured = ", ".join(f"{s}: {meta[s]['url']}" for s in used)
    file = spec["file"]
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(spec['title'])}</title>
<!--
  AI READY WISCONSIN · {spec['code']} · Explore: See It in Action · interactive demo player
  Every AI response below is a REAL, unedited T.I.T.A.N. - Prime transcript, captured {spec['captured']}
  (math notation reformatted for the web). Built by _explore/build.py from _explore/pages/{name}.yaml and
  _explore/captures/{name}.json — edit those, not this file. Sessions: {captured}
  EPISODE SLOT: when the filmed episode exists, add its embed inside #episodeSlot and set style="display:block".
  Canvas embed: <iframe src="{SITE}{file}" width="100%" height="2400" style="border:0;" title="{html.escape(spec['title'])}"></iframe>
-->
<style>{css}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">

  <div class="panel hero">
    <div class="hero-flex">
      <div class="lockup"><strong>AI READY WISCONSIN</strong><span>University of Wisconsin Oshkosh</span></div>
      <div style="flex:1; min-width: 250px;">
        <h1>{spec['title']}</h1>
        <p class="sub"><strong>{spec['sub']}</strong> {spec.get('icon', '🎬')}</p>
        <p class="meta"><strong>Estimated time:</strong> {spec['time']} &nbsp;·&nbsp; {spec['module']}</p>
      </div>
    </div>
  </div>

  <div id="episodeSlot" style="display: none; margin-bottom: 26px;"><!-- filmed episode embed goes here later --></div>

  <div class="panel dark">
    <div class="sec-head"><div class="icon-circle" aria-hidden="true">🎬</div><h2>Before you press play</h2></div>
    <div class="card">
{paras(spec['before'])}
    </div>
  </div>

  <div class="real-note">{spec['real_note']}</div>

  <div class="player" id="player">
    <div class="player-head">
      <span class="scene-tag" id="sceneTag">SCENE 1</span>
      <h3 id="sceneTitle"></h3>
      <div class="dots" id="dots" aria-label="Scene progress"></div>
    </div>
    <div class="player-body" id="sceneBody" aria-live="polite"></div>
    <div class="player-nav">
      <button class="nav-btn ghost" id="prevBtn" type="button">← Back</button>
      <button class="nav-btn" id="nextBtn" type="button">Next scene →</button>
    </div>
  </div>

  <div class="panel dark">
    <div class="sec-head"><div class="icon-circle" aria-hidden="true">🎯</div><h2>What to take into your lab</h2></div>
    <div class="card">
{paras(spec['takeaway'])}
    </div>
  </div>

  <div class="gold-note" style="margin-bottom: 26px;">
    <p style="font-size: 17px; text-align: center;"><strong>{spec['next']}</strong></p>
  </div>

  <div class="footer-note">This page follows <a href="https://www.w3.org/TR/WCAG21/" target="_blank" rel="noopener" aria-label="Web Content Accessibility Guidelines WCAG 2.1 (opens in a new tab)">Web Content Accessibility Guidelines (WCAG) 2.1</a>.</div>
  <div class="brand-foot">AI READY WISCONSIN &nbsp;·&nbsp; UNIVERSITY OF WISCONSIN OSHKOSH</div>

</div>
{PLAYER_JS.replace('%SCENES%', json.dumps(scenes, ensure_ascii=False, indent=1).replace('</', '<\\/'))}
</body>
</html>
"""
    out = ROOT / file
    out.write_text(page, encoding="utf-8")
    # the Canvas page body, laid out exactly like M01_P03's
    canvas = f"""<div style="max-width: 900px; margin: 0 auto; font-family: Arial, sans-serif;">
<div style="background: linear-gradient(135deg, #ffcc00 0%, #fcb414 100%); padding: 24px 30px; border-radius: 10px; margin-bottom: 18px;">
<h2 style="color: #000000; font-size: 26px; margin: 0 0 6px 0;">🎬 {spec['title']}</h2>
<p style="color: #000000; font-size: 15px; margin: 0;"><strong>{spec['sub']}</strong> &nbsp;·&nbsp; Estimated time: {spec['time']}. Predict what the AI will do before each answer appears — every response is a real, unedited T.I.T.A.N. conversation.</p>
</div>
<iframe src="{SITE}{file}" width="100%" height="2600" style="border: 0; border-radius: 10px;" title="{html.escape(spec['title'])} — interactive demo" loading="lazy"></iframe>
<div style="background: #f5f5f5; border-radius: 10px; padding: 16px 20px; margin-top: 18px;">
<p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6;"><strong>Not loading, or want more room?</strong> <a href="{SITE}{file}" target="_blank">Open the demo in a new tab</a>. When you finish the reel, head to the next page — the AI Lab — where you press the buttons yourself.</p>
</div>
</div>"""
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.canvas.html").write_text(canvas, encoding="utf-8")
    return out


# ---------------------------------------------------------------- educator blocks (Canvas inline)

S = {
    "label": "font-size:.78em;color:#8a6a00;margin:0 0 .5em;",
    "h3": "font-size:1.08em;margin:1.5em 0 .4em;color:#1a1a1a;",
    "p": "line-height:1.6;margin:0 0 .85em;color:#1a1a1a;",
    "frame": "border:1px solid #d8dce2;border-left:6px solid #1a1a1a;border-radius:3px;padding:1em 1.15em;margin:1em 0 1.4em;background:#ffffff;",
    "you": "background:#f4f5f7;border:1px solid #d8dce2;border-radius:3px;padding:.75em 1em;margin:.4em 0 .8em;font-family:Consolas,Monaco,monospace;font-size:.9em;line-height:1.5;color:#1a1a1a;",
    "ai": "border-left:3px solid #ffcc00;padding:.2em 0 .2em 1em;margin:.6em 0 1em;color:#1a1a1a;line-height:1.55;",
    # the reveal matches the educator Learn pages' own "Reveal:" boxes
    "details": "background:#ffffff;padding:1em 1.2em;border-radius:10px;border:2px solid #ffcc00;margin:.4em 0 1em;",
    "summary": "cursor:pointer;color:#000000;font-size:1.05em;font-weight:bold;",
    "notice": "background:#fff7db;border-left:6px solid #ffcc00;padding:1em 1.15em;margin:1em 0 .4em;",
}


def style_ai(h: str) -> str:
    h = tidy(h)
    h = re.sub(r"<p>", f'<p style="margin:0 0 .7em;">', h)
    h = re.sub(r"<li>", '<li style="margin:0 0 .4em;">', h)
    h = re.sub(r"<(ul|ol)>", r'<\1 style="margin:0 0 .8em;padding-left:1.3em;">', h)
    h = h.replace("<hr>", '<hr style="border:none;border-top:1px dashed #d8dce2;margin:.8em 0;">')
    h = h.replace('<span class="math">', '<span style="font-family:Consolas,Monaco,monospace;">')
    h = h.replace("<table>", '<table style="border-collapse:collapse;margin:0 0 .8em;font-size:.95em;" border="1">')
    h = re.sub(r"<(th|td)>", r'<\1 style="padding:.4em .55em;border:1px solid #d8dce2;text-align:left;vertical-align:top;">', h)
    return h


def you_block(h: str) -> str:
    text = re.sub(r"</p>\s*<p>", "\n", tidy(h))
    text = re.sub(r"<br>", "\n", text)
    text = re.sub(r"</?p>", "", text).strip()
    return f'<p style="{S["you"]}white-space:pre-wrap;">{text}</p>'


def build_educator(name: str, spec: dict) -> Path:
    sess, meta = turns(name) if spec.get("blocks") else ({}, {})
    blocks = []
    for blk in spec.get("blocks") or []:
        parts = [f'<div style="{S["frame"]}">',
                 f'<p style="{S["label"]}">{spec["label"]}</p>',
                 f'<h3 style="{S["h3"]}margin-top:0;">{blk["heading"]}</h3>']
        parts += [f'<p style="{S["p"]}">{x}</p>' for x in blk.get("intro", [])]
        for step in blk["steps"]:
            you = ref(sess, step["prompt"])
            ai = ref(sess, step["ai"])
            if step.get("show_prompt", True):
                parts.append(f'<p style="{S["p"]}margin-bottom:.2em;"><strong>{step.get("prompt_label", "The prompt")}</strong></p>')
                parts.append(you_block(you["html"]))
            # the notes sit inside the reveal: the prompt asks the reader to decide what to check first
            notice = (f'<div style="{S["notice"]}"><p style="{S["label"]}">What to notice</p>'
                      + "".join(f'<p style="line-height:1.55;margin:0 0 .6em;">{x}</p>' for x in step["notice"]) + "</div>"
                      ) if step.get("notice") else ""
            parts.append(f'<details style="{S["details"]}"><summary style="{S["summary"]}">{step["reveal"]}</summary>'
                         f'<div style="{S["ai"]}">{style_ai(ai["html"])}</div>{notice}</details>')
        parts.append("</div>")
        blocks.append({"after": blk["after"], "html": "".join(parts)})
    OUT.mkdir(exist_ok=True)
    out = OUT / f"{name}.canvas.json"
    out.write_text(json.dumps({"page": spec["canvas_page"], "remove_slot": True, "blocks": blocks,
                               "replace": spec.get("replace") or []},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / f"{name}.preview.html").write_text(
        "<!DOCTYPE html><meta charset=utf-8><title>%s preview</title><body style=\"font-family:Arial,sans-serif;max-width:52em;margin:2em auto;padding:0 16px;\">%s</body>"
        % (name, "".join(b["html"] for b in blocks)), encoding="utf-8")
    return out


def main(argv):
    names = argv or sorted(p.stem for p in (HERE / "pages").glob("*.yaml"))
    for n in names:
        spec = yaml.safe_load((HERE / "pages" / f"{n}.yaml").read_text(encoding="utf-8"))
        out = build_student(n, spec) if n.startswith("s-") else build_educator(n, spec)
        print(n, "→", out.relative_to(ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
