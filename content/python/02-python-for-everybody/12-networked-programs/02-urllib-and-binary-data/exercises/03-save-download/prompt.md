The server on your own computer (started by the tests) hands out files that are not text. Write `download(url, dest)` that fetches the file at `url`, saves its exact bytes into the file at path `dest`, and returns the number of bytes saved. `dest` is a `pathlib.Path`.

```python
n = download(base + "/pic.bin", tmp_path / "pic.bin")
```

The saved file must be byte-for-byte identical to what the server sent, including an empty file.
