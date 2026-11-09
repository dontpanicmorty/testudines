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


from solution import status_line


def test_ok(addr):
    host, port = addr
    assert status_line(host, port, "/hello") == "HTTP/1.0 200 OK"


def test_not_found(addr):
    host, port = addr
    assert status_line(host, port, "/missing") == "HTTP/1.0 404 Not Found"


def test_other_page(addr):
    host, port = addr
    assert status_line(host, port, "/note") == "HTTP/1.0 200 OK"


def test_no_line_ending_left(addr):
    host, port = addr
    line = status_line(host, port, "/hello")
    assert "\r" not in line and "\n" not in line
