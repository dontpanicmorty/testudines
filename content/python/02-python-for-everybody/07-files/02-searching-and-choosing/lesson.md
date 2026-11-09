+++
id = "everybody.files.searching-and-choosing"
title = "Searching files and handling missing ones"
minutes = 24
+++

# Searching files and handling missing ones

Most programs do not need every line in a file. They look for the interesting lines and ignore the rest. This lesson shows how to do that, and how to cope when a file is not there.

## Our example file

A made-up server log, `server.log`:

```
INFO start
WARN disk 91%
INFO user ana joined
ERROR db timeout

WARN retrying
```

## Picking out lines

Use an `if` inside the loop, with a string method that asks a yes/no question about the line.

```python
handle = open("server.log", encoding="utf-8")
for line in handle:
    line = line.rstrip()
    if line.startswith("WARN"):
        print(line)
handle.close()
```

Step by step: each `line` still has its newline, so `rstrip()` removes it. Then `startswith("WARN")` is `True` only for warnings. Only those get printed.

## Skipping lines with continue

You can flip the logic: skip what you do not want and process the rest. The `continue` statement jumps to the next line of the file.

```python
for line in handle:
    line = line.rstrip()
    if line == "":
        continue
    if "disk" not in line:
        continue
    print(line)
```

Two quick skips keep the main work easy to read, with no deep nesting.

## Searching and extracting

Combine these with what you know about strings to pull numbers out:

```python
total = 0
for line in handle:
    if line.startswith("WARN disk"):
        percent = line.rstrip().split()[-1]   # "91%"
        total += int(percent.rstrip("%"))
```

Notice `rstrip("%")`. Giving `rstrip` a character removes that character from the end instead of blanks.

## Letting the user choose the file

A program is more useful if the person running it names the file. Normally you would ask with `input`:

```python
name = input("Which file? ")
handle = open(name, encoding="utf-8")
```

The function-based exercises here receive the name as an argument instead. That is the same idea, and it is easier to test.

## When the file is missing

People mistype names. Without protection, the program crashes with a `FileNotFoundError`. Use `try` and `except` around the `open` call.

```python
name = "nofile.txt"
try:
    handle = open(name, encoding="utf-8")
except FileNotFoundError:
    print("Sorry, I cannot find", name)
    handle = None
```

The `except` block runs only if opening fails. After it, the program carries on, so you must decide what happens next. For example, return early, ask again, or exit.

```python
def count_errors(name):
    try:
        handle = open(name, encoding="utf-8")
    except FileNotFoundError:
        return None
    count = 0
    for line in handle:
        if line.startswith("ERROR"):
            count += 1
    handle.close()
    return count
```

Returning `None` means "no answer", which is different from the honest answer `0`.

## Common mistakes

- Forgetting `rstrip()`, so that `line == "ERROR"` is never true because the line is `"ERROR\n"`.
- Putting the whole loop inside `try`, which hides unrelated bugs. Wrap only `open`.
- Catching every error with a bare `except:`. Name `FileNotFoundError`.
- Using `continue` and then forgetting to put the real work after the skips.
- Case: `"warn"` does not start `"WARN disk"`.
