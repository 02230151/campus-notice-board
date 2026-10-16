import json, os, socket, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

START = time.time()
VERSION = os.environ.get("APP_VERSION", "1.0.0")
STUDENT = os.environ.get("STUDENT_ID", "unknown")
BROKEN = os.environ.get("BROKEN", "false").lower() == "true"
WARMUP_SECONDS = 5
HAS_CATEGORY = not VERSION.startswith("1.0")   # 1.1.0 and later add category/pinned

NOTICES = [
    {"id": 1, "title": "Library hours extended", "body": "Open until 10pm during exams."},
    {"id": 2, "title": "Hostel fee deadline", "body": "Pay before the 30th."},
    {"id": 3, "title": "Guest lecture on DevOps", "body": "Friday 2pm, Hall B."},
]
if HAS_CATEGORY:
    NOTICES[0].update({"category": "academic", "pinned": False})
    NOTICES[1].update({"category": "finance", "pinned": True})
    NOTICES[2].update({"category": "events", "pinned": False})


def notices_payload():
    # Flag is read from the environment at start-up (matters for Task 8)
    pinned_first = HAS_CATEGORY and os.environ.get("FEATURE_PINNED", "false").lower() == "true"
    items = list(NOTICES)
    if pinned_first:
        items.sort(key=lambda n: not n.get("pinned", False))  # stable: pinned first
    return {"pinnedFirst": pinned_first, "notices": items}


def healthy():
    if BROKEN:
        return False                       # 1.2.0-broken never becomes healthy
    return (time.time() - START) >= WARMUP_SECONDS   # warm-up simulation


class Handler(BaseHTTPRequestHandler):
    def send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/notices":
            self.send(200, notices_payload())
        elif self.path == "/version":
            self.send(200, {"version": VERSION, "student": STUDENT, "pod": socket.gethostname()})
        elif self.path == "/healthz":
            ok = healthy()
            self.send(200 if ok else 503, {"status": "ok" if ok else "unhealthy"})
        else:
            self.send(404, {"error": "not found"})

    def log_message(self, *args):
        pass  # keep container logs quiet; the monitor makes a request every 0.5s


ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()