import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from solution import stations_with_bikes

PAYLOAD = {"results": [
    {"name": "Mill Lane", "bikes": 4},
    {"name": "Quay Street", "bikes": 0},
    {"name": "Hill Top", "bikes": 9},
]}


@pytest.fixture
def base_url():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps(PAYLOAD).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/stations"
    server.shutdown()
    server.server_close()


def test_minimum_one(base_url):
    assert stations_with_bikes(base_url, 1) == ["Mill Lane", "Hill Top"]


def test_minimum_zero(base_url):
    assert stations_with_bikes(base_url, 0) == ["Mill Lane", "Quay Street", "Hill Top"]


def test_nothing_matches(base_url):
    assert stations_with_bikes(base_url, 100) == []
