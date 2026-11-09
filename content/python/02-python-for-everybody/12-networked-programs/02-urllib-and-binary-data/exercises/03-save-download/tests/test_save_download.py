import socketserver
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

        server = _LocalServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
        servers.append(server)
        return "http://127.0.0.1:%d" % server.server_address[1]

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()


from solution import download


class _LocalServer(http.server.ThreadingHTTPServer):
    """A test web server on 127.0.0.1. It skips the network-name lookup that HTTPServer does when it
    starts, which can stall for seconds on some machines, and the tests only ever use the address."""

    def server_bind(self):
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]

PAYLOAD = b"\x89PNG\r\n\x1a\n" + bytes(range(256)) * 8 + b"\x00\xff"


def test_bytes_identical(serve, tmp_path):
    base = serve({"/pic.bin": ("application/octet-stream", PAYLOAD)})
    dest = tmp_path / "pic.bin"
    count = download(base + "/pic.bin", dest)
    assert dest.read_bytes() == PAYLOAD
    assert count == len(PAYLOAD)


def test_empty_file(serve, tmp_path):
    base = serve({"/e.bin": ("application/octet-stream", b"")})
    dest = tmp_path / "e.bin"
    assert download(base + "/e.bin", dest) == 0
    assert dest.read_bytes() == b""


def test_text_file_unchanged(serve, tmp_path):
    base = serve({"/t.txt": ("text/plain", "a\r\nb\n")})
    dest = tmp_path / "t.txt"
    download(base + "/t.txt", dest)
    assert dest.read_bytes() == b"a\r\nb\n"


def test_larger_than_one_chunk(serve, tmp_path):
    big = bytes(range(256)) * 400
    base = serve({"/big": ("application/octet-stream", big)})
    dest = tmp_path / "big"
    assert download(base + "/big", dest) == len(big)
    assert dest.read_bytes() == big
