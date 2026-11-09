import socketserver
import threading

import pytest

PAGES = {
    "/hello": "Hello from the tiny server\n",
    "/note": "Line one\nLine two\nLine three\n",
}


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        request_line = self.rfile.readline().decode("latin-1").strip()
        while True:
            line = self.rfile.readline()
            if line in (b"", b"\r\n", b"\n"):
                break
        parts = request_line.split()
        path = parts[1] if len(parts) > 1 else "/"
        if parts[:1] == ["GET"] and path in PAGES:
            body = PAGES[path].encode("utf-8")
            status = "HTTP/1.0 200 OK"
        else:
            body = b"nothing here\n"
            status = "HTTP/1.0 404 Not Found"
        head = (
            status + "\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "Content-Length: " + str(len(body)) + "\r\n"
            "X-Served-By: testudines-test\r\n"
            "\r\n"
        )
        self.wfile.write(head.encode("latin-1") + body)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


@pytest.fixture
def addr():
    server = Server(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield server.server_address[0], server.server_address[1]
    server.shutdown()
    server.server_close()


from solution import page_text


def test_hello(addr):
    host, port = addr
    assert page_text(host, port, "/hello") == "Hello from the tiny server\n"


def test_multiline(addr):
    host, port = addr
    assert page_text(host, port, "/note").splitlines() == ["Line one", "Line two", "Line three"]


def test_missing_page_body(addr):
    host, port = addr
    assert page_text(host, port, "/nope") == "nothing here\n"


def test_no_headers_in_body(addr):
    host, port = addr
    assert "HTTP/1.0" not in page_text(host, port, "/hello")
