+++
id = "everybody.networked-programs.http-and-sockets"
title = "How the web talks: HTTP and sockets"
minutes = 30
+++

# How the web talks: HTTP and sockets

When you type an address into a browser, a conversation happens between two programs. Your browser is the **client**. A computer somewhere else, running a **web server**, is the other side. They talk in a shared language called **HTTP** (HyperText Transfer Protocol). A **protocol** is just an agreed set of rules for a conversation, like "you say hello first, then I answer".

> **Offline note.** Addresses such as `http://example.org/` appear in this lesson only to explain ideas. The exercises never use the internet. The checking program starts a tiny web server on your own computer (address `127.0.0.1`, which always means "this machine") and your code talks to that one.

## Requests and responses

HTTP is a question and an answer.

1. The client sends a **request**: "please give me this page".
2. The server sends a **response**: a status, some extra information, and then the page itself.

A very small request looks like this:

```
GET /hello HTTP/1.0
Host: example.org

```

- `GET` is the **method**: "fetch something".
- `/hello` is the **path**: which thing on that server.
- `HTTP/1.0` is the version of the language.
- `Host:` is a **header**, one line of extra information in the form `Name: value`.
- A **blank line** ends the request.

The response begins with a **status line**, then headers, a blank line, and the **body**:

```
HTTP/1.0 200 OK
Content-Type: text/plain
Content-Length: 12

Hello there!
```

The status line holds the version, a three-digit **status code** and a short reason. The codes you will meet most:

- `200 OK`: here is what you asked for.
- `404 Not Found`: no such page.
- `403 Forbidden`: you are not allowed.
- `500 Internal Server Error`: the server broke.

The body is whatever the page contains: text, HTML, or the bytes of an image.

## A socket is a telephone line

To talk to another computer, a Python program opens a **socket**: a two-way connection. It needs the server's **host** (a name like `example.org`, or an address like `127.0.0.1`) and a **port**, a number saying which program on that computer to talk to. Web servers normally listen on port 80 (or 443 for the secure kind).

## The simplest browser

Here is a complete client that fetches one page.

```python
import socket

mysock = socket.create_connection(("127.0.0.1", 8000))
request = "GET /hello HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n"
mysock.sendall(request.encode())

reply = b""
while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    reply = reply + data
mysock.close()

print(reply.decode())
```

Step by step:

- `create_connection` dials the host and port and gives back the socket.
- `\r\n` is the line ending HTTP uses (a "carriage return" and a "line feed"). The final `\r\n\r\n` is the blank line that ends the request.
- Sockets carry **bytes**, not text. `.encode()` turns text into bytes for sending, and `.decode()` turns the bytes you received back into text.
- `recv(512)` waits for up to 512 bytes. The server may send the page in several pieces, so we loop and join the pieces.
- When the server has finished and closed its end, `recv` returns empty bytes, and we stop.

## Splitting headers from body

The reply is one block of bytes. The headers and body are separated by the first blank line, `\r\n\r\n`.

```python
head, _, body = reply.partition(b"\r\n\r\n")
lines = head.decode().split("\r\n")
print(lines[0])      # HTTP/1.0 200 OK
print(lines[1:])     # the headers
print(body.decode()) # the page
```

`partition` splits a string or bytes value at the first match of the separator and gives three pieces: before, the separator, after. Notice the separator is also bytes, written `b"..."`.

To read headers as a dictionary, split each line at the first colon:

```python
headers = {}
for line in lines[1:]:
    name, _, value = line.partition(":")
    headers[name.strip().lower()] = value.strip()
```

We lowercase names because header names do not care about capital letters.

## Debugging connections

- `ConnectionRefusedError` means nobody is listening at that host and port. Check the port number.
- If your program hangs, the server may be waiting for the blank line that ends the request.
- Print the whole `reply` first. Read it with your own eyes before you start splitting it.
- A `UnicodeDecodeError` means the body is not text, for example it is an image. Keep it as bytes.

## Common mistakes

- Sending a `str` instead of bytes: `sendall("GET ...")` fails; use `.encode()`.
- Leaving out the final blank line of the request.
- Using `\n` in one place and `\r\n` in another.
- Calling `.decode()` on the whole reply when it contains an image.
