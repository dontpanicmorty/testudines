+++
id = "files-and-formats.pathlib-and-text-files"
title = "Paths and text files"
minutes = 25
+++

# Paths and text files

Every pipeline starts and ends with files: an export lands in a stage, a log gets written, a rejects file goes to a human. In SQL you say `COPY INTO @stage/...` and the warehouse handles bytes. In Python *you* handle the path, the encoding and the cleanup.

> **SQL bridge.** A stage path like `@raw/orders/2025-06-01.csv` is a location plus a name. `pathlib.Path` is the same idea: an object that knows how to join, inspect and open a location.

## Path objects, not strings

Old code glues strings together with `+` and `"/"`. That breaks on Windows and invites typos. Use `Path` and the `/` operator.

```python
from pathlib import Path

base = Path("data") / "raw" / "orders_2025-06-01.csv"
print(base)
print(base.name)     # file name with extension
print(base.stem)     # name without the last extension
print(base.suffix)   # .csv
print(base.parent)   # data/raw
print(base.with_suffix(".parquet"))
```

A `Path` is just a value. Nothing touches the disk until you ask: `exists()`, `read_text()`, `mkdir()`.

## Writing and reading text

We will work in a temporary directory so examples leave nothing behind.

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "note.txt"
    p.write_text("line one\nline two\n", encoding="utf-8")
    print(p.exists(), p.stat().st_size, "bytes")
    text = p.read_text(encoding="utf-8")
    print(repr(text))
    print(text.splitlines())
```

`write_text` and `read_text` are perfect for small files. Always pass `encoding="utf-8"`. Without it Python picks the operating system default, and your code behaves differently on a laptop and in a container.

## `with open(...)`: streaming and cleanup

Big files should not be loaded whole. `open` gives you a file object you can loop over one line at a time. The `with` block guarantees the file is closed, even if an exception fires inside.

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "log.txt"
    with p.open("w", encoding="utf-8") as f:
        for i in range(3):
            f.write(f"event {i}\n")
    with p.open(encoding="utf-8") as f:
        for line in f:                 # one line at a time, constant memory
            print(line.rstrip("\n"))
```

Modes: `"r"` read (default), `"w"` write (**truncates an existing file**), `"a"` append, `"x"` create and fail if it exists. Add `"b"` for bytes.

> **Predict first.** What does `len(line)` return for `"event 0\n"`? Is it 7 or 8?

```python
line = "event 0\n"
print(len(line), len(line.rstrip("\n")))
```

Iterating a file keeps the trailing newline. Forgetting to strip it is behind half of the "why does my last column have a weird value" bugs.

## Encodings and newlines

Files are bytes; text is what you get after decoding. UTF-8 handles every character, but exports from spreadsheets often arrive as UTF-8 with a BOM, which shows up as a stray `﻿` glued to the first header.

```python
raw = "﻿id,name\n1,Zoë\n".encode("utf-8")
print(raw[:3])                          # the BOM bytes
print(repr(raw.decode("utf-8").splitlines()[0]))
print(repr(raw.decode("utf-8-sig").splitlines()[0]))   # BOM removed
```

Use `encoding="utf-8-sig"` when reading files that may come from Excel. When decoding fails you get `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 ...`: the file is probably Latin-1. Decide deliberately; do not silently ignore errors.

Newlines: Windows writes `\r\n`, Unix `\n`. In text mode Python translates both to `\n` on read. When you write CSV files with the `csv` module, open with `newline=""` so it controls line endings itself (next lesson).

## Temporary directories in tests

Tests must not write into your repository. pytest gives you a fresh empty directory per test through the `tmp_path` fixture, which is a `Path`.

```python
# no-run   (this is a test, run it with pytest)
def test_writes_report(tmp_path):
    out = tmp_path / "report.txt"
    write_report(out, ["a", "b"])
    assert out.read_text(encoding="utf-8") == "a\nb\n"
```

Design functions to **accept a path** instead of hardcoding one. That is what makes them testable.

## Finding files

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    (root / "2025").mkdir()
    (root / "2025" / "a.csv").write_text("x", encoding="utf-8")
    (root / "2025" / "b.csv").write_text("x", encoding="utf-8")
    (root / "notes.txt").write_text("x", encoding="utf-8")
    print(sorted(p.name for p in root.glob("*.txt")))
    print(sorted(p.relative_to(root).as_posix() for p in root.rglob("*.csv")))
```

`glob` matches one level, `rglob` recurses. Sort the result; directory order is not guaranteed.

## Common mistakes

- Opening with `"w"` on a file you meant to append to. The old contents are gone.
- `FileNotFoundError: [Errno 2] No such file or directory: 'data/in.csv'`: the path is relative to where the program was *started*, not where the script lives. Build paths from a known base.
- Forgetting `parents=True` in `mkdir(parents=True, exist_ok=True)` and getting `FileNotFoundError` on the nested folder.
- Reading a multi-gigabyte file with `read_text()`. Iterate instead.

## What to take away

1. Use `Path` and `/`; read and write with `encoding="utf-8"` every time.
2. `with` closes files for you; iterate a file to stream it.
3. Iterated lines keep `\n`; use `utf-8-sig` for Excel exports.
4. Functions take paths as arguments; tests use `tmp_path`.
5. Sort `glob` results before relying on order.
