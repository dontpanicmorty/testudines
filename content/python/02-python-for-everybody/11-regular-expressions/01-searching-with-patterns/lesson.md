+++
id = "everybody.regular-expressions.searching-with-patterns"
title = "Searching with patterns"
minutes = 30
+++

# Searching with patterns

Suppose you have a thousand lines of text and want the ones that mention a phone number. `in` can check for an exact piece of text like `"555"`, but it cannot say "three digits, a dash, then four digits". For that you need a **regular expression**, often shortened to **regex**. A regex is a small pattern written in a special mini-language. It describes the *shape* of text you are looking for.

Python's tools for this live in a module called `re`.

```python
import re
```

## `re.search`

`re.search(pattern, text)` looks through `text` for the first place where the pattern fits. It returns a **match object** if it finds one, and `None` if it does not. Because `None` counts as false in an `if`, you can use it directly.

```python
import re

line = "Order 42 shipped"
if re.search("ship", line):
    print("found it")
```

With plain letters, a pattern simply means those letters, so this is the same as `"ship" in line`. The power comes from special characters.

A tip: write patterns as **raw strings**, with an `r` before the opening quote, like `r"\d"`. In a raw string Python leaves backslashes alone, so the regex sees exactly what you typed.

## Character matching: the building blocks

Each of these matches something about the text.

- `^` matches the **start** of the line.
- `$` matches the **end** of the line.
- `.` matches **any one character** (except a newline).
- `\d` matches one **digit**, `0` to `9`.
- `\s` matches one **whitespace** character (space, tab, newline).
- `\S` matches one **non-whitespace** character.
- `[abc]` matches **one** character from the list; `[a-z]` is a range; `[0-9]` is the digits.
- `[^abc]` matches one character that is **not** in the list.

```python
print(bool(re.search(r"^Order", "Order 42")))     # True
print(bool(re.search(r"^Order", "My Order 42")))  # False: not at the start
print(bool(re.search(r"\d", "abc3")))             # True
print(bool(re.search(r"c.t", "a cat")))           # True: . matches the a
```

(`bool(...)` turns the match object into `True` or `False` for printing.)

## Repeating things

These mark the item just before them as repeating.

- `*` means **zero or more** times.
- `+` means **one or more** times.
- `?` means **zero or one** time (it makes the item optional).

```python
print(bool(re.search(r"^\d+$", "2026")))     # True: only digits, all the way
print(bool(re.search(r"^\d+$", "20x6")))     # False
print(bool(re.search(r"colou?r", "color")))  # True: the u is optional
print(bool(re.search(r"^S\S*", "Sam")))      # True
```

Read `^\d+$` as: start of text, one or more digits, end of text. Together, `^` and `$` make a pattern match the **whole** line instead of just a piece.

## Looking at what matched

A match object remembers the text that matched. `.group()` gives it back.

```python
m = re.search(r"\d+", "Order 42 shipped")
print(m.group())     # 42
```

Always check for `None` first. Calling `.group()` on `None` crashes with an `AttributeError`.

```python
m = re.search(r"\d+", "no numbers here")
if m:
    print(m.group())
else:
    print("nothing")
```

## A worked example

Which of these lines are error lines? Those starting with `ERROR`.

```python
lines = ["INFO ok", "ERROR disk full", "WARN: ERROR soon"]
for line in lines:
    if re.search(r"^ERROR", line):
        print(line)
```

Only the middle line prints. Without the `^`, the third line would match as well.

## Debugging a pattern

Build a pattern in small steps. Start with something that matches too much and tighten it. Test with a few strings you know should match and a few that should not. Print the match object, or `m.group()`, to see what the pattern really caught: it is often not what you expected.

## Common mistakes

- Forgetting to check for `None` before using `.group()`.
- Forgetting `^` and `$`, so the pattern matches a piece in the middle of a longer string.
- Writing patterns without the `r` prefix, so `"\d"` may behave oddly.
- Expecting `[abc]` to match the three letters in a row. It matches exactly one of them.
- Forgetting that `.` means any character, not a literal dot (the next lessons fix that).
