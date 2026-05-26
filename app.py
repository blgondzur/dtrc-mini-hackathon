#!/usr/bin/env python3
"""
Room Booker — local web app, zero external dependencies.
Run: python3 app.py
Then open: http://localhost:8765
"""

import http.server
import json
import sqlite3
import os
import re
from urllib.parse import urlparse, parse_qs

_DATA_DIR = os.path.join(os.path.expanduser("~"), ".room-booker")
os.makedirs(_DATA_DIR, exist_ok=True)
DB_PATH   = os.path.join(_DATA_DIR, "bookings.db")
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")


# ── Database ──────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS rooms (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            capacity    INTEGER,
            location    TEXT    DEFAULT '',
            description TEXT    DEFAULT '',
            amenities   TEXT    DEFAULT '',
            created_at  TEXT    DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS bookings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id     INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
            booked_by   TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            start_time  TEXT    NOT NULL,
            end_time    TEXT    NOT NULL,
            purpose     TEXT    DEFAULT '',
            status      TEXT    DEFAULT 'confirmed',
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


# ── Request Handler ───────────────────────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # suppress default console noise

    def send_json(self, data, status=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n)) if n else {}

    def serve_html(self):
        with open(HTML_PATH, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ── GET ───────────────────────────────────────────────────────────────────

    def do_GET(self):
        p = urlparse(self.path)
        path, qs = p.path, parse_qs(p.query)

        if path in ("/", "/index.html"):
            self.serve_html()

        elif path == "/api/rooms":
            conn = get_db()
            rows = conn.execute("SELECT * FROM rooms ORDER BY name").fetchall()
            conn.close()
            self.send_json([dict(r) for r in rows])

        elif path == "/api/bookings":
            conn = get_db()
            room_id = qs.get("room_id", [None])[0]
            date    = qs.get("date",    [None])[0]
            sql = """
                SELECT b.*, r.name AS room_name
                FROM bookings b JOIN rooms r ON b.room_id = r.id
                WHERE b.status = 'confirmed'
            """
            params = []
            if room_id:
                sql += " AND b.room_id = ?"; params.append(room_id)
            if date:
                sql += " AND b.date = ?";    params.append(date)
            sql += " ORDER BY b.date, b.start_time"
            rows = conn.execute(sql, params).fetchall()
            conn.close()
            self.send_json([dict(r) for r in rows])

        else:
            self.send_json({"error": "not found"}, 404)

    # ── POST ──────────────────────────────────────────────────────────────────

    def do_POST(self):
        path = urlparse(self.path).path
        data = self.read_json()

        if path == "/api/rooms":
            name = (data.get("name") or "").strip()
            if not name:
                return self.send_json({"error": "name is required"}, 400)
            conn = get_db()
            cur = conn.execute(
                "INSERT INTO rooms (name, capacity, location, description, amenities) VALUES (?,?,?,?,?)",
                (name,
                 data.get("capacity") or None,
                 data.get("location", ""),
                 data.get("description", ""),
                 data.get("amenities", ""))
            )
            conn.commit()
            row = conn.execute("SELECT * FROM rooms WHERE id=?", (cur.lastrowid,)).fetchone()
            conn.close()
            self.send_json(dict(row), 201)

        elif path == "/api/bookings":
            for f in ["room_id", "booked_by", "date", "start_time", "end_time"]:
                if not data.get(f):
                    return self.send_json({"error": f"{f} is required"}, 400)
            if data["start_time"] >= data["end_time"]:
                return self.send_json({"error": "End time must be after start time"}, 400)

            conn = get_db()
            conflict = conn.execute("""
                SELECT id FROM bookings
                WHERE room_id=? AND date=? AND status='confirmed'
                  AND start_time < ? AND end_time > ?
            """, (data["room_id"], data["date"], data["end_time"], data["start_time"])).fetchone()
            if conflict:
                conn.close()
                return self.send_json({"error": "Room is already booked during that time"}, 409)

            cur = conn.execute(
                "INSERT INTO bookings (room_id, booked_by, date, start_time, end_time, purpose) VALUES (?,?,?,?,?,?)",
                (data["room_id"], data["booked_by"], data["date"],
                 data["start_time"], data["end_time"], data.get("purpose", ""))
            )
            conn.commit()
            row = conn.execute(
                "SELECT b.*, r.name AS room_name FROM bookings b JOIN rooms r ON b.room_id=r.id WHERE b.id=?",
                (cur.lastrowid,)
            ).fetchone()
            conn.close()
            self.send_json(dict(row), 201)

        else:
            self.send_json({"error": "not found"}, 404)

    # ── PATCH ─────────────────────────────────────────────────────────────────

    def do_PATCH(self):
        path = urlparse(self.path).path
        m = re.match(r"^/api/bookings/(\d+)/cancel$", path)
        if m:
            conn = get_db()
            conn.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (m.group(1),))
            conn.commit()
            conn.close()
            self.send_json({"ok": True})
        else:
            self.send_json({"error": "not found"}, 404)

    # ── DELETE ────────────────────────────────────────────────────────────────

    def do_DELETE(self):
        path = urlparse(self.path).path
        m = re.match(r"^/api/rooms/(\d+)$", path)
        if m:
            conn = get_db()
            conn.execute("DELETE FROM rooms WHERE id=?", (m.group(1),))
            conn.commit()
            conn.close()
            self.send_json({"ok": True})
        else:
            self.send_json({"error": "not found"}, 404)

    # ── OPTIONS (CORS preflight) ───────────────────────────────────────────────

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    PORT = 8765
    server = http.server.HTTPServer(("localhost", PORT), Handler)
    print(f"\n  Room Booker  →  http://localhost:{PORT}\n")
    print("  Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
