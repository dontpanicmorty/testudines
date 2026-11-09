+++
id = "everybody.files.opening-and-reading"
title = "Opening and reading files"
minutes = 22
+++

# Opening and reading files

So far, everything your programs know disappears when they finish. Variables live in memory, and memory is cleared when the program ends. To keep information, a program must save it somewhere that lasts. Storage that survives is called **persistence**, and the most common kind is a **file** on your disk.

## Text files

A **text file** holds plain characters, like a note you could open in a basic editor. This lesson uses a made-up file called `pantry.txt`:

```
flour 2
sugar 1
rice 5
```

## Opening a file

Before reading, you ask Python to open the file. The `open` function returns a **file handle**, a kind of connection to the file. The handle is not the contents. It is the way you get at them.

```python
handle = open("pantry.txt", encoding="utf-8")
print(handle)
```

The second piece, `encoding="utf-8"`, tells Python how characters are stored as bytes. UTF-8 is the common choice, and naming it avoids surprises with accented letters or symbols on different computers.

If the file does not exist, Python stops with a `FileNotFoundError`. Later you will learn to catch that.

When you finish with a file, close it with `handle.close()`. The next lesson shows a tidier way.

## Lines and the newline character

Inside a text file, the end of each line is marked by a hidden character called a **newline**. In Python it is written `"\n"`. The file above really looks like this:

```
flour 2\nsugar 1\nrice 5\n
```

Remember this. It explains many surprises, such as extra blank lines when you print.

## Reading line by line

A file handle can be used directly in a `for` loop. Each iteration gives you the next line as a string.

```python
handle = open("pantry.txt", encoding="utf-8")
for line in handle:
    print(line)
handle.close()
```

This prints the three lines with a blank line after each. Why? The `line` still ends in a newline, and `print` adds its own. Cure it by removing the newline with `rstrip()`, which cuts blank characters off the right-hand end.

```python
for line in handle:
    print(line.rstrip())
```

Reading this way is efficient: Python fetches one line at a time, so even a huge file works.

## Reading everything at once

The `read` method returns the whole file as one big string, newlines included.

```python
handle = open("pantry.txt", encoding="utf-8")
text = handle.read()
handle.close()
print(len(text))
print(text.split("\n"))
```

Use `read` for small files. For large ones, loop over the lines instead. Once you have read a handle to the end, it is used up: a second `read` gives an empty string `""` unless you reopen the file.

## Counting lines

Combining the loop and the counter pattern:

```python
count = 0
handle = open("pantry.txt", encoding="utf-8")
for line in handle:
    count += 1
handle.close()
print(count)   # 3
```

## Common mistakes

- Forgetting `rstrip()` and getting a blank line after each printed line.
- Calling `read` twice on the same handle and wondering why the second result is empty.
- Mixing up the handle (the connection) with the text it gives you.
- Opening a file name that is spelled wrongly or lives in a different folder.
- Forgetting `encoding="utf-8"`, which can garble non-English letters.
