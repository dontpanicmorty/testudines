A small web server is listening on `host` and `port` (the tests start it on your own computer; nothing touches the internet). Write `status_line(host, port, path)` that uses a **socket** to send a `GET` request for `path` and returns the first line of the server's reply as text, without line ending, for example `"HTTP/1.0 200 OK"`.

The server understands the paths `/hello` and `/note`. Any other path gives a `404` reply.
