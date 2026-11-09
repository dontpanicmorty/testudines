+++
id = "iteration-and-idioms.reading-tracebacks"
title = "Reading tracebacks"
minutes = 30
+++

# Reading tracebacks

You will spend a surprising fraction of your career staring at error output. The engineers who look fast are not guessing better; they read the traceback methodically and then shrink the problem until the cause is obvious. This lesson gives you that routine.

> **SQL bridge.** A failed query gives you one line and a position: `SQL compilation error: Object 'ORDRS' does not exist`. A Python traceback is the same information plus the **path of calls** that led there.

## Anatomy of a traceback

```text
Traceback (most recent call last):
  File "pipeline.py", line 14, in <module>
    result = summarise(rows)
  File "pipeline.py", line 9, in summarise
    return total / count
ZeroDivisionError: division by zero
```

Read it in this order:

1. **Last line first.** The exception type (`ZeroDivisionError`) says *what kind* of failure; the message says *what value or name*.
2. **The line just above it** is where it blew up: `return total / count`, in function `summarise`.
3. **Work upward** only if the cause is not at that line. Each pair above is the caller: who called `summarise`, with what.

"Most recent call last" means the bottom frame is the nearest to the crash. The top frames are your program's entry points. Frames inside library code (paths with `site-packages`) are usually not your bug; find the **lowest frame in your own code** and start there.

## The common exceptions, with their real messages

Learn to recognise these on sight. Each snippet below is marked `# no-run` because it fails on purpose; the message shown is what Python prints.

```python
# no-run
print(total)
```

```text
NameError: name 'total' is not defined
```
Typo, or the variable was defined in a different scope, or the code that defines it never ran.

```python
# no-run
"id-" + 7
```

```text
TypeError: can only concatenate str (not "int") to str
```
Wrong type for the operation. Also: `TypeError: 'NoneType' object is not subscriptable` (you indexed `None`; an earlier function returned nothing), and `TypeError: f() missing 1 required positional argument: 'x'`.

```python
# no-run
int("12.5")
```

```text
ValueError: invalid literal for int() with base 10: '12.5'
```
Right type, wrong content. The message even shows the offending value, which is gold when parsing messy files.

```python
# no-run
row = {"id": 1}
row["email"]
```

```text
KeyError: 'email'
```
The key is missing. Print `row.keys()` to see what is there; check spelling, case and whitespace (`"Email "` is not `"email"`).

```python
# no-run
rows = []
rows[0]
```

```text
IndexError: list index out of range
```
Empty list, or an off-by-one. Check `len(rows)` first.

```python
# no-run
value = None
value.strip()
```

```text
AttributeError: 'NoneType' object has no attribute 'strip'
```
The most common error in data code: something you expected to be text is `None` (a NULL, a failed lookup, or a function that forgot to `return`). Work out where the `None` came from.

```python
# no-run
total / len([])
```

```text
ZeroDivisionError: division by zero
```
An average over zero rows. Guard the empty case.

```python
# no-run
open("exports/orders.csv")
```

```text
FileNotFoundError: [Errno 2] No such file or directory: 'exports/orders.csv'
```
Wrong path or wrong working directory. Print `os.getcwd()` and the absolute path you built.

Two honourable mentions: `SyntaxError` (code is malformed, often a missing colon or bracket, reported on or just above the line shown) and `ModuleNotFoundError: No module named 'pandas'` (wrong environment, or a typo in the import).

## Catching errors on purpose

Reading errors is for bugs. For **expected** failures, such as one bad row in a feed, catch the specific exception:

```python
def to_amount(text):
    try:
        return float(text)
    except ValueError:
        return None

print([to_amount(t) for t in ["1.5", "N/A", "3"]])
```

Catch the narrowest type you can. A bare `except:` hides real bugs, including typos. To keep the failure details, bind the exception:

```python
try:
    int("x")
except ValueError as exc:
    print(type(exc).__name__, "->", exc)
```

## Print-debugging done well

The cheapest debugger is a good `print`. Make it informative:

```python
rows = [{"id": 1, "amount": "10"}, {"id": 2, "amount": None}]
for row in rows:
    print("DEBUG row:", repr(row), type(row["amount"]))
```

Use `repr()` (or the `!r` f-string flag: `f"{value!r}"`) so you can see quotes, whitespace and `None`. `print(x)` shows `5` for both the int `5` and the string `"5"`; `repr` doesn't. Print the **type** and the **length** too. Delete the prints (or switch to `logging`) when done.

## The REPL and pdb mindset

Don't re-run a 10-minute pipeline to test one idea. Reproduce the failing step on a **tiny input** in a REPL or scratch file, and poke at it: what is the value, what is its type, what does this method return?

For stepping inside a failing function, drop in a breakpoint:

```python
# no-run
def summarise(rows):
    breakpoint()          # drops into pdb right here
    return sum(r["amount"] for r in rows) / len(rows)
```

At the `(Pdb)` prompt: `p expr` prints a value, `n` runs the next line, `s` steps into a call, `c` continues, `w` shows where you are in the stack, `q` quits. You don't need more than those six.

## A systematic debugging checklist

1. **Read the last line.** Say what it means out loud, in plain words.
2. **Find the lowest frame in your own code** and read that line.
3. **Check your assumptions about the data.** Print `repr`, `type`, `len` of each value on that line.
4. **Shrink the input** to the smallest row or file that still fails.
5. **Form one hypothesis, change one thing, re-run.** Never change several things at once.
6. **Suspect `None`, whitespace, case and types** before suspecting Python.
7. **Fix the cause, not the symptom**; adding `try/except` around a bug only hides it.
8. **Add a test** with the failing input so it cannot come back.

## Common mistakes

- Reading the top of the traceback instead of the bottom.
- Blaming the library: the lowest frame in *your* code is almost always the culprit.
- Fixing a `KeyError` by wrapping in `try/except: pass` and silently losing rows.
- Using `print(x)` where `print(repr(x))` would have revealed the stray space.
- Changing three things between runs, so you don't know which one mattered.

## What to take away

1. Read tracebacks bottom-up: exception type and message, then the line, then callers.
2. Learn the eight classics: `NameError`, `TypeError`, `ValueError`, `KeyError`, `IndexError`, `AttributeError`, `ZeroDivisionError`, `FileNotFoundError`.
3. Use `repr`, `type` and `len` in debug prints; shrink the input.
4. Catch the narrowest exception, only for expected failures.
5. Follow the checklist: one hypothesis, one change, then add a test.
