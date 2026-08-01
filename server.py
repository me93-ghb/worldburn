#!/usr/bin/env python3
"""Serve the site plus /api/fires.csv, a cached proxy for NASA FIRMS.

FIRMS publishes keyless rolling CSVs of global active-fire detections.
The proxy exists because FIRMS sends no CORS headers and because one cached
upstream fetch should serve every visitor rather than one per browser.
"""
import functools
import http.server
import threading
import time
import urllib.request
from pathlib import Path

FIRMS_URL = ("https://firms.modaps.eosdis.nasa.gov/data/active_fire/"
             "modis-c6.1/csv/MODIS_C6_1_Global_7d.csv")
CACHE_TTL = 30 * 60  # FIRMS updates continuously; half an hour is fresh enough here
PORT = 8123

_cache = {"t": 0.0, "data": b""}
_lock = threading.Lock()


def get_fires() -> bytes:
    with _lock:
        if time.time() - _cache["t"] > CACHE_TTL:
            req = urllib.request.Request(FIRMS_URL, headers={"User-Agent": "worldburn"})
            try:
                _cache["data"] = urllib.request.urlopen(req, timeout=120).read()
                _cache["t"] = time.time()
            except OSError:
                if not _cache["data"]:  # no stale copy to fall back on
                    raise
        return _cache["data"]


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/api/fires":
            return super().do_GET()
        try:
            data = get_fires()
        except OSError as e:
            self.send_error(502, f"FIRMS fetch failed: {e}")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/csv")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    handler = functools.partial(Handler, directory=str(root))
    http.server.ThreadingHTTPServer(("", PORT), handler).serve_forever()
