import socket


def status_line(host, port, path):
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
    return reply.decode("latin-1").split("\r\n")[0]
