import socket


def reply_headers(host, port, path):
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
    lines = head.decode("latin-1").split("\r\n")
    headers = {}
    for line in lines[1:]:
        name, _, value = line.partition(":")
        headers[name.strip().lower()] = value.strip()
    return headers
