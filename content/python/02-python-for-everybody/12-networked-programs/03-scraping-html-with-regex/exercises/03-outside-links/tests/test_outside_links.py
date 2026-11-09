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


from solution import outside_links

PAGE = """<html><body>
<a href="/news.html">news</a>
<a href="http://example.org/maps">maps</a>
<a href="https://example.net/b">b</a>
<a href="http://example.org/maps">maps again</a>
<a href="mailto:hi@example.org">mail</a>
</body></html>"""


def test_collects_sorted_unique(serve):
    base = serve({"/": ("text/html", PAGE)})
    assert outside_links(base + "/") == ["http://example.org/maps", "https://example.net/b"]


def test_no_outside_links(serve):
    base = serve({"/p": ("text/html", '<a href="/only">x</a>')})
    assert outside_links(base + "/p") == []


def test_empty_page(serve):
    base = serve({"/e": ("text/html", "")})
    assert outside_links(base + "/e") == []


def test_returns_list(serve):
    base = serve({"/": ("text/html", PAGE)})
    assert isinstance(outside_links(base + "/"), list)
