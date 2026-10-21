"""Save a captured Playlab session from the Claude Code session log (the browser tool's own result).

usage: from_log.py <session.jsonl> <page> <id> <playlab-session-suffix> [note]

Finds the newest browser-tool result that is a JSON string {"at", "url", "turns"} whose url ends with
the given Playlab session suffix, and appends it to _explore/captures/<page>.json via add_session.py.
"""
import json
import subprocess
import sys
from pathlib import Path

log, page, sid, suffix = sys.argv[1:5]
note = sys.argv[5:] and sys.argv[5] or ""
found = None
for line in Path(log).read_text(encoding="utf-8").splitlines():
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        continue
    content = d.get("message", {}).get("content")
    if not isinstance(content, list):
        continue
    for c in content:
        if c.get("type") != "tool_result":
            continue
        parts = c.get("content")
        texts = [parts] if isinstance(parts, str) else [p.get("text", "") for p in parts or [] if isinstance(p, dict)]
        for t in texts:
            # the result is a JSON string literal, possibly after a batch prefix and before the tool's tab notes
            i = t.find('"{\\"at\\"')
            while i >= 0:
                try:
                    s = json.loads(json.JSONDecoder().raw_decode(t, i)[0])
                    if s.get("url", "").endswith(suffix):
                        found = s
                except (json.JSONDecodeError, TypeError):
                    pass
                i = t.find('"{\\"at\\"', i + 1)
if not found:
    sys.exit(f"no capture ending {suffix} in {log}")
tmp = Path(__file__).parent / "captures" / f".incoming-{page}-{sid}.json"
tmp.write_text(json.dumps(found, ensure_ascii=False), encoding="utf-8")
r = subprocess.run([sys.executable, str(Path(__file__).parent / "add_session.py"), page, sid, str(tmp), *([note] if note else [])])
tmp.unlink(missing_ok=True)
sys.exit(r.returncode)
