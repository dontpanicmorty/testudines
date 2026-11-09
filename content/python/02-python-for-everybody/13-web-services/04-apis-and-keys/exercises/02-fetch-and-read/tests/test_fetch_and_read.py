import socketserver
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from solution import stations_with_bikes


class _LocalServer(HTTPServer):
    """A test web server on 127.0.0.1. It skips the network-name lookup that HTTPServer does when it
    starts, which can stall for seconds on some machines, and the tests only ever use the address."""

    def server_bind(self):
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]

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

    server = _LocalServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
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
