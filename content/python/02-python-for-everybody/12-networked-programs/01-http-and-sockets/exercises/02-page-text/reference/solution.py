import socket


def page_text(host, port, path):
    sock = socket.create_connection((host, port), timeout=5)
    request = "GET " + path + " HTTP/1.0\r\nHost: " + host + "\r\n\r\n"
    sock.sendall(request.encode())
    reply = b""
    while True:
        data = sock.recv(512)
        if len(data) < 1:
            break
        reply += data
    sock.close()
    head, _, body = reply.partition(b"\r\n\r\n")
    return body.decode("utf-8")
