import http.server
import threading

import pytest


@pytest.fixture
def serve(monkeypatch):
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    servers = []

    def start(pages):
        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.0"

            def do_GET(self):
                page = pages.get(self.path)
                if page is None:
                    status, ctype, body = 404, "text/plain", b"not found"
                else:
                    status, (ctype, body) = 200, page
                    if isinstance(body, str):
                        body = body.encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        servers.append(server)
        return "http://127.0.0.1:%d" % server.server_address[1]

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()


from solution import fetch_or_none


def test_found(serve):
    base = serve({"/x": ("text/plain", "hello")})
    assert fetch_or_none(base + "/x") == "hello"


def test_missing(serve):
    base = serve({"/x": ("text/plain", "hello")})
    assert fetch_or_none(base + "/y") is None


def test_empty_page_is_not_none(serve):
    base = serve({"/e": ("text/plain", "")})
    assert fetch_or_none(base + "/e") == ""


def test_root_missing(serve):
    base = serve({})
    assert fetch_or_none(base + "/") is None
