+++
id = "everybody.regular-expressions.extracting-with-findall"
title = "Extracting data with findall"
minutes = 25
+++

# Extracting data with findall

`re.search` answers "is there a match, and what is the first one?". Often you want **every** match. That is the job of `re.findall(pattern, text)`. It returns a **list of strings**, one for each match, and an empty list if there are none.

## Finding all the numbers

```python
import re

text = "Rooms 12, 7 and 130 are free."
print(re.findall(r"\d+", text))     # ['12', '7', '130']
```

What happens here: the pattern `\d+` means "one or more digits". `findall` scans from left to right. It finds `12`, carries on after it, finds `7`, then `130`.

The results are strings. Convert them if you want numbers:

```python
numbers = [int(n) for n in re.findall(r"\d+", text)]
print(sum(numbers))      # 149
```

Because an empty list is false, `if re.findall(...)` also tells you "was there anything?".

## Matching sets of characters

Square brackets are the workhorse for extraction. Some useful sets:

- `[a-z]` lowercase letters, `[A-Z]` capitals, `[0-9]` digits.
- `[A-Za-z0-9_]` letters, digits and underscores (you can combine ranges).
- `[^ ]` anything but a space.
- `\S` is a shortcut for "anything but whitespace".

Pull out all the words that start with `#`:

```python
tweet = "Loving #python and #learning_to_code today!"
print(re.findall(r"#[A-Za-z0-9_]+", tweet))
# ['#python', '#learning_to_code']
```

Notice the `!` and the spaces are not in the set, so they stop each match.

Words that look like email addresses, very roughly:

```python
text = "write to ana@example.org or ben@example.com"
print(re.findall(r"\S+@\S+", text))
# ['ana@example.org', 'ben@example.com']
```

`\S+` grabs as many non-space characters as it can on each side of the `@`.

## Greedy matching

By default, repeating symbols like `*` and `+` are **greedy**: they grab as much text as they possibly can, as long as the whole pattern still fits.

```python
text = '"red" and "blue"'
print(re.findall(r'".*"', text))
# ['"red" and "blue"']
```

You might have wanted `"red"` and `"blue"` separately. But `.*` is greedy: starting at the first quote, it swallows everything up to the **last** quote in the line, and then the closing `"` matches there. One big match.

## Non-greedy matching

Add a `?` after the repeat to make it **non-greedy**: it takes as little as possible.

```python
print(re.findall(r'".*?"', text))
# ['"red"', '"blue"']
```

Now `.*?` stops at the first closing quote that lets the pattern finish. This is why a `?` appears in two roles: after a character it means "optional", and after `*` or `+` it means "be non-greedy".

Another way to avoid greed is to be more precise. `"[^"]*"` means a quote, then any number of non-quote characters, then a quote. That cannot run past the next quote.

```python
print(re.findall(r'"[^"]*"', text))
# ['"red"', '"blue"']
```

## Patterns that find nothing

If `findall` returns `[]`, check these in order:

1. Did you use a raw string?
2. Is the text what you think? Print it.
3. Is a part of your pattern too strict? Remove the last piece and try again.

## Debugging by shrinking

Take a short sample of the real text, copy it into a variable, and try the simplest pattern first. Add one piece at a time. If your result suddenly gets worse after adding something, you have found the culprit.

## Common mistakes

- Expecting integers back. `findall` always gives strings.
- Using greedy `.*` between two markers on a line with several pairs.
- Forgetting that the spaces matter: `\d+ \d+` needs exactly one space between the numbers.
- Using `findall` when you only need the first match; `search` is clearer then.
