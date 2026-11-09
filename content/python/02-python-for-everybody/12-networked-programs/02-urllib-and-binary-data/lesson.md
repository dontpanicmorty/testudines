+++
id = "everybody.networked-programs.urllib-and-binary-data"
title = "Pages and files with urllib"
minutes = 25
+++

# Pages and files with urllib

Opening a socket by hand teaches how the web works, but nobody wants to do it for every page. Python's `urllib.request` module does the whole conversation for you: it connects, sends the request, removes the headers and hands you the body.

> **Offline note.** Web addresses like `http://example.org/page.html` are used in this lesson as illustrations. The exercises talk to a tiny server the checking program starts on your own computer.

## Reading a page

```python
import urllib.request

response = urllib.request.urlopen("http://127.0.0.1:8000/hello")
data = response.read()
print(data)
```

`urlopen` takes a **URL** (a web address) and gives back a response object that works a bit like an open file. `.read()` returns the body as **bytes**, and the printout starts with `b'...'` to show that.

To get text, decode the bytes:

```python
text = data.decode("utf-8")
print(text)
```

UTF-8 is the usual way to turn characters into bytes, and the one most pages use.

You can also loop over the response line by line, as with a file. Each line is bytes, so decode each one.

```python
response = urllib.request.urlopen("http://127.0.0.1:8000/note")
for line in response:
    print(line.decode("utf-8").rstrip())
```

It is also polite to close a response when you finish. A `with` block does it for you:

```python
with urllib.request.urlopen(url) as response:
    text = response.read().decode("utf-8")
```

## Status and headers

The response also knows what the server said about the page.

```python
with urllib.request.urlopen(url) as response:
    print(response.status)                        # 200
    print(response.headers["Content-Type"])       # text/plain; charset=utf-8
```

## When things go wrong

If the server answers with an error status like 404, `urlopen` raises an exception called `urllib.error.HTTPError`. If it cannot reach the server at all, you get `urllib.error.URLError`. Because `HTTPError` is a kind of `URLError`, catching `URLError` catches both. Use `try` / `except` just as you did for other errors.

```python
import urllib.error
import urllib.request

try:
    with urllib.request.urlopen(url) as response:
        text = response.read().decode("utf-8")
except urllib.error.HTTPError as err:
    print("server said", err.code)
```

## Binary data: images and other files

Not everything on the web is text. A picture, a PDF or a zip file is **binary data**: bytes that do not spell out characters. If you try `.decode("utf-8")` on a picture, Python will usually fail with a `UnicodeDecodeError`. For binary data, keep the bytes and never decode them.

Counting how many bytes arrived:

```python
with urllib.request.urlopen(url) as response:
    data = response.read()
print(len(data), "bytes")
```

`len()` of bytes counts bytes, not characters.

## Saving to a file

To save the bytes, open a file in **write binary** mode, `"wb"`. The `b` means no text conversion happens.

```python
with open("picture.png", "wb") as out:
    out.write(data)
```

For a very large file you would not read everything into memory at once. Instead you read a small piece at a time and write each piece:

```python
with urllib.request.urlopen(url) as response:
    with open("big.bin", "wb") as out:
        while True:
            chunk = response.read(4096)
            if len(chunk) < 1:
                break
            out.write(chunk)
```

`read(4096)` returns up to 4096 bytes, and an empty result means the data is finished. The same loop pattern as the socket lesson, but much shorter.

## Debugging

- Print `type(data)` to tell bytes from text.
- Check `len(data)` against the `Content-Length` header if you have doubts.
- Open the saved file in a viewer to confirm it is not damaged. A common cause of a damaged image is opening the file with `"w"` instead of `"wb"`.
- If your program hangs, the address may be wrong. Servers can be slow, so real programs set a `timeout`.

## Common mistakes

- Forgetting `.decode()` and getting `b'...'` text in your output.
- Decoding an image as text.
- Writing binary data to a file opened with `"w"`. That raises a `TypeError`.
- Not catching `HTTPError` when a page might be missing.
