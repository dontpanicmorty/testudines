#!/usr/bin/env python3
"""Static file server for SQL Dojo that disables caching, so a plain reload in
Safari always picks up the latest edits instead of serving a stale copy."""
import http.server
import os
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        pass  # keep the terminal quiet; start.sh prints the one line that matters


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    http.server.ThreadingHTTPServer(('', port), NoCacheHandler).serve_forever()
