+++
id = "everybody.files.writing-and-with"
title = "Writing files, with, and invisible characters"
minutes = 24
+++

# Writing files, with, and invisible characters

Reading files is half the story. Programs also need to save their results.

## Opening a file for writing

Add a second piece to `open`, called the **mode**. The mode `"w"` means write.

```python
out = open("shopping.txt", "w", encoding="utf-8")
out.write("eggs\n")
out.write("milk\n")
out.close()
```

Three things to notice:

- If `shopping.txt` does not exist, Python creates it. If it does exist, `"w"` **erases it first**. Be careful.
- `write` puts exactly the characters you give it into the file. It does not add a newline for you, so you add `"\n"` yourself.
- `write` accepts only strings. Convert numbers with `str()` or use an f-string: `out.write(f"{count}\n")`.

The mode `"a"` means append: it keeps the old contents and adds new text at the end. The default mode, when you give none, is `"r"` for read.

## Why close matters

Python may hold your text in memory for a moment before writing it to disk. `close()` makes sure everything is saved. If your program forgets to close, some text may be lost, or another program may see an unfinished file.

## The with statement

Remembering to close is easy to forget, especially if an error happens halfway. The `with` statement does the closing for you, even if there is an error.

```python
with open("shopping.txt", "w", encoding="utf-8") as out:
    out.write("eggs\n")
    out.write("milk\n")
```

When the indented block ends, the file is closed automatically. Reading looks the same:

```python
with open("shopping.txt", encoding="utf-8") as handle:
    for line in handle:
        print(line.rstrip())
```

From now on, prefer `with`. The name after `as` is the handle, just as before.

## Writing from data

A common job is to take a list and save it, one item per line:

```python
items = ["eggs", "milk", "tea"]
with open("shopping.txt", "w", encoding="utf-8") as out:
    for item in items:
        out.write(item + "\n")
```

## Debugging: the invisible characters

File bugs are often caused by things you cannot see: spaces at the end of a line, tabs, newlines, a blank last line. Python has a helper called `repr` that shows a value the way you would type it in code.

```python
line = "milk  \n"
print(line)          # looks like: milk
print(repr(line))    # 'milk  \n'
```

The `repr` output reveals two trailing spaces and the newline. When a comparison such as `line == "milk"` fails for no clear reason, print `repr(line)` and look closely.

Other habits:

- Print `len(line)` to detect extra characters.
- Open the file in a text editor that shows whitespace.
- Test on a tiny file you made yourself.

## Common mistakes

- Opening an important file with `"w"` and wiping it.
- Forgetting the `"\n"` and getting all text on one line.
- Passing a number to `write` without converting it.
- Leaving out `with` or `close()`.
- Trusting how `print` looks instead of checking with `repr`.
