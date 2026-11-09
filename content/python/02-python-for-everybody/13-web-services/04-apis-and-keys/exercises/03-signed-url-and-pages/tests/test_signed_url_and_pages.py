import socketserver
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from solution import collect_items, make_request_url


class _LocalServer(HTTPServer):
    """A test web server on 127.0.0.1. It skips the network-name lookup that HTTPServer does when it
    starts, which can stall for seconds on some machines, and the tests only ever use the address."""

    def server_bind(self):
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]


def test_url_has_key_last():
    assert make_request_url("http://x.test/a", {"q": "oak"}, {"PLACE_API_KEY": "k1"}) == "http://x.test/a?q=oak&key=k1"


def test_url_escapes():
    url = make_request_url("http://x.test/a", {"q": "a b"}, {"PLACE_API_KEY": "k&1"})
    assert url == "http://x.test/a?q=a+b&key=k%261"


def test_missing_key():
    with pytest.raises(RuntimeError):
        make_request_url("http://x.test/a", {}, {})


@pytest.fixture
def server():
    state = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            base = state["base"]
            pages = {
                "/p1": {"items": [1, 2], "next": base + "/p2"},
                "/p2": {"items": [3], "next": base + "/p3"},
                "/p3": {"items": [], "next": None},
                "/single": {"items": ["only"], "next": None},
            }
            body = json.dumps(pages[self.path]).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    httpd = _LocalServer(("127.0.0.1", 0), Handler)
    state["base"] = f"http://127.0.0.1:{httpd.server_port}"
    thread = threading.Thread(target=httpd.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    thread.start()
    yield state["base"]
    httpd.shutdown()
    httpd.server_close()


def test_follows_pages(server):
    assert collect_items(server + "/p1") == [1, 2, 3]


def test_single_page(server):
    assert collect_items(server + "/single") == ["only"]
