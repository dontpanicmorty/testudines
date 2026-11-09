A small web server is listening on `host` and `port` (the tests start it on your own computer). Write `page_text(host, port, path)` that uses a **socket** to request `path` and returns **only the body** of the reply, as text (UTF-8). The headers must not be included. A page that does not exist still has a body, so return it too.

The server serves `/hello` and `/note`.
