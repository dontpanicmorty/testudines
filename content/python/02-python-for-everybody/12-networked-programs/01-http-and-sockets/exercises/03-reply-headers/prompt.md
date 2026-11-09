A small web server is listening on `host` and `port` (started by the tests on your own computer). Write `reply_headers(host, port, path)` that uses a **socket** to request `path` and returns the reply's headers as a dictionary. Names must be lowercase and both names and values must have surrounding spaces removed. The status line is not a header and must not be in the dictionary.

For example a header line `Content-Type: text/plain; charset=utf-8` becomes the entry `"content-type": "text/plain; charset=utf-8"`.
