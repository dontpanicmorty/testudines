+++
id = "everybody.strings.parsing-and-f-strings"
title = "Parsing text and f-strings"
minutes = 24
+++

# Parsing text and f-strings

Real data often arrives as a line of text with the interesting part buried inside. **Parsing** means picking out the piece you want. Once you have it, you often need to put values back into a sentence. For that, Python has f-strings.

## Parsing with find and slices

Suppose you have a made-up log line:

```python
line = "ERROR 2025-03-14 disk full"
```

To get the word `ERROR`, find the first blank and slice up to it:

```python
space = line.find(" ")
level = line[:space]
print(level)   # ERROR
```

To get the message at the end, slice from just after the last blank. Here is a pattern for text between two markers:

```python
text = "name=[Avery];age=31"
start = text.find("[")
end = text.find("]", start)
print(text[start + 1:end])   # Avery
```

Step by step: `find("[")` gives the position of the opening bracket. We look for the closing bracket starting from there. We slice one past the opening bracket (so we skip the bracket itself) up to, but not including, the closing one.

## Parsing with split

When the pieces are separated by a known character, `split` is often easier:

```python
parts = "ERROR 2025-03-14 disk full".split(" ", 2)
print(parts)   # ['ERROR', '2025-03-14', 'disk full']
```

The second number limits the number of cuts, so the rest stays together in the last piece.

Text pieces are still strings. Turn digits into numbers with `int()` or `float()`:

```python
year = int("2025-03-14".split("-")[0])
print(year + 1)   # 2026
```

## Formatted string literals

Joining text and values with `+` gets clumsy, because numbers must be converted first. An **f-string** is a string with an `f` before the opening quote. Anything inside curly braces is worked out and put into the text.

```python
name = "Avery"
age = 31
print(f"{name} is {age} years old")
print(f"next year: {age + 1}")
```

The braces can hold any expression. You can also control how a number looks after a colon:

```python
price = 3.14159
print(f"{price:.2f}")     # 3.14   (two decimal places)
print(f"{7:03d}")         # 007    (pad with zeros to width 3)
print(f"{'hi':>6}|")      #     hi| (right-aligned in 6 spaces)
```

If you need a literal brace, double it: `f"{{done}}"` prints `{done}`.

## Debugging with strings

Text bugs are often invisible. These habits help:

- Print values with `repr`, as in `print(repr(text))`. It shows quotes and hidden characters such as `\n`.
- Check `len(text)`. A stray space makes the length one too big.
- When a slice is wrong, print the numbers you used (`start`, `end`) before slicing.
- Test with the smallest line that shows the problem.

## Common mistakes

- Forgetting the `f` at the front, so the braces print literally.
- Forgetting that `find` returns `-1` when the marker is missing, giving a surprising slice.
- Off-by-one slices that include the marker character.
- Doing arithmetic on text pieces without converting them with `int()` first.
