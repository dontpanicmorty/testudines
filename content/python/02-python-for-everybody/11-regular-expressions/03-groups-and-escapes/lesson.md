+++
id = "everybody.regular-expressions.groups-and-escapes"
title = "Groups, escapes and a syntax summary"
minutes = 30
+++

# Groups, escapes and a syntax summary

So far a match has been the whole piece of text the pattern covers. Often you only want **part** of it. Take the line `Total: $42.50`. The pattern needs to include the words `Total: $`, but you only want the number. **Groups** solve this.

## Parentheses make groups

Put round brackets `( )` around the part of the pattern you want to extract.

```python
import re

line = "Total: $42.50"
m = re.search(r"Total: \$(\d+\.\d\d)", line)
print(m.group())     # Total: $42.50   (the whole match)
print(m.group(1))    # 42.50           (what the first brackets caught)
```

`.group()` or `.group(0)` is the whole match. `.group(1)` is the text matched by the first pair of brackets, `.group(2)` the second, and so on, counting opening brackets from the left.

This combines **searching** (find the right line) with **extracting** (take out only the piece you need).

```python
m = re.search(r"^From: (\S+)@(\S+)$", "From: ana@example.org")
if m:
    print(m.group(1))    # ana
    print(m.group(2))    # example.org
```

`m.groups()` returns all groups at once as a tuple: `('ana', 'example.org')`.

## Groups with findall

When the pattern has exactly **one group**, `findall` returns only what the group matched.

```python
text = "ana@example.org, ben@example.com"
print(re.findall(r"\S+@(\S+)", text))
# ['example.org,', 'example.com']
```

That list also holds a trailing comma, because `\S` matches commas. Be precise: `[a-z.]+` matches only letters and dots.

```python
print(re.findall(r"[a-z]+@([a-z.]+)", text))
# ['example.org', 'example.com']
```

With two or more groups, `findall` returns a list of tuples, one tuple per match.

```python
print(re.findall(r"(\w+)=(\d+)", "a=1 b=22"))
# [('a', '1'), ('b', '22')]
```

(`\w` is a shortcut for a "word character": a letter, digit or underscore.)

## Escape characters

Some characters have a special meaning in a pattern: `. ^ $ * + ? ( ) [ ] { } | \`. What if you want to match one **literally**? Put a backslash in front of it. This is called **escaping**.

```python
print(re.findall(r"\$\d+", "cost $5, then $30"))   # ['$5', '$30']
print(re.findall(r"\.", "a.b.c"))                  # ['.', '.']
print(re.findall(".", "a.b"))                      # ['a', '.', 'b']
```

Without the backslash, `.` matches *any* character and `$` means end-of-line. A very common bug is matching a version number such as `3.11` with `3.11`: the dot would also match `3x11`.

Inside square brackets most characters lose their special powers, so `[.]` and `[$]` also mean a literal dot and dollar sign.

## Summary table

| Symbol | Meaning |
| --- | --- |
| `^` | start of the line |
| `$` | end of the line |
| `.` | any one character |
| `\s` / `\S` | one whitespace / one non-whitespace character |
| `\d` | one digit |
| `\w` | one letter, digit or underscore |
| `*` | repeat zero or more times |
| `+` | repeat one or more times |
| `?` | optional (zero or one time) |
| `*?` `+?` | non-greedy versions of `*` and `+` |
| `[abc]` | one of the listed characters |
| `[a-z]` | one character in the range |
| `[^abc]` | one character not in the list |
| `( )` | a group: the part to extract |
| `\` | escape: treat the next symbol literally |

## Debugging groups

Print `m.groups()` to see what every group caught. If `.group(1)` returns something odd, count the opening brackets again. If a group did not take part in the match, `.group(n)` is `None`.

## Common mistakes

- Using `.group(1)` when the pattern has no brackets: `IndexError: no such group`.
- Forgetting to escape a literal dot or dollar sign.
- Expecting `findall` to return whole matches when the pattern has a group.
- Using greedy `.*` inside a group and catching too much.
