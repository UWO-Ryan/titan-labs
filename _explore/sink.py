"""Local receiver for Playlab captures (127.0.0.1 only).

GET  /helpers.js                 → playlab-helpers.js, for injecting into the Playlab tab
POST /save?page=<p>&id=<s>[&note=…]  body {"at", "url", "turns": [html, …]} → _explore/captures/<p>.json
"""
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        if urlparse(self.path).path != "/helpers.js":
            self.send_response(404); self._cors(); self.end_headers(); return
        body = (HERE / "playlab-helpers.js").read_bytes()
        self.send_response(200); self._cors()
        self.send_header("Content-Type", "text/javascript; charset=utf-8"); self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        q = parse_qs(urlparse(self.path).query)
        page, sid, note = q["page"][0], q["id"][0], q.get("note", [""])[0]
        data = self.rfile.read(int(self.headers["Content-Length"]))
        tmp = HERE / "captures" / f".incoming-{page}-{sid}.json"
        tmp.write_bytes(data)
        r = subprocess.run([sys.executable, str(HERE / "add_session.py"), page, sid, str(tmp), *([note] if note else [])],
                           capture_output=True, text=True, encoding="utf-8")
        tmp.unlink(missing_ok=True)
        msg = (r.stdout + r.stderr).strip().encode("utf-8")
        self.send_response(200 if r.returncode == 0 else 500); self._cors()
        self.send_header("Content-Type", "text/plain; charset=utf-8"); self.end_headers()
        self.wfile.write(msg)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8766), H).serve_forever()
