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


from solution import allowed_links

HOME = """<html><body>
<a href="/public/a.html">a</a>
<a href="/private/x.html">x</a>
<a name="anchor-only">no address</a>
<a href="/public/b.html">b</a>
<a href="/admin">admin</a>
</body></html>"""


def test_respects_robots(serve):
    robots = "User-agent: *\nDisallow: /private/\nDisallow: /admin\n"
    base = serve({"/robots.txt": ("text/plain", robots), "/": ("text/html", HOME)})
    assert allowed_links(base) == ["/public/a.html", "/public/b.html"]


def test_no_robots_file(serve):
    base = serve({"/": ("text/html", HOME)})
    assert allowed_links(base) == [
        "/public/a.html",
        "/private/x.html",
        "/public/b.html",
        "/admin",
    ]


def test_empty_disallow_forbids_nothing(serve):
    base = serve({"/robots.txt": ("text/plain", "User-agent: *\nDisallow:\n"), "/": ("text/html", HOME)})
    assert len(allowed_links(base)) == 4


def test_page_without_links(serve):
    base = serve({"/": ("text/html", "<p>nothing</p>")})
    assert allowed_links(base) == []
