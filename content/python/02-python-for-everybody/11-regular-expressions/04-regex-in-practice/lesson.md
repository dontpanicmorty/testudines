+++
id = "everybody.regular-expressions.regex-in-practice"
title = "Regular expressions in practice"
minutes = 25
+++

# Regular expressions in practice

You now know the pieces. This lesson shows how they fit into everyday programs: searching files for lines, pulling data out of them, and fixing patterns that misbehave.

## A grep-like search (a bonus aside)

On many computers there is a command-line tool called **grep** whose name stands for "global regular expression print". You give it a pattern and a file and it prints every line that matches. You can write the same thing in a few lines of Python.

```python
import re

def grep(path, pattern):
    found = []
    with open(path) as handle:
        for line in handle:
            line = line.rstrip()
            if re.search(pattern, line):
                found.append(line)
    return found

print(grep("server.log", r"^ERROR"))
```

How it works: each line is stripped of its trailing newline with `.rstrip()`, tested with `re.search`, and kept if it matches. You get back the matching lines as a list.

Because the function takes the pattern as a parameter, it is a flexible little tool. Try `r"timeout"`, `r"\d\d:\d\d"` or `r"^$"` (empty lines).

## Searching and extracting together

A very common shape of program is: loop over lines, check each with a pattern that has a group, use the group.

```python
import re

total = 0
count = 0
with open("server.log") as handle:
    for line in handle:
        m = re.search(r"took (\d+) ms", line)
        if m:
            total += int(m.group(1))
            count += 1
if count:
    print(total / count)
```

Walk through it: lines without `took N ms` give `None` and are skipped. Matching lines add their number to the total. The `if count:` guard avoids dividing by zero when nothing matched.

## Finding the same shape many times

If an address looks like four numbers separated by dots, the pattern needs escapes for the dots.

```python
text = "hosts: 10.0.0.1 and 192.168.1.20"
print(re.findall(r"\d+\.\d+\.\d+\.\d+", text))
# ['10.0.0.1', '192.168.1.20']
```

This is a loose pattern: it also accepts `999.1.1.1`. For exploring text, loose is often good enough. For checking that input is valid, check the numbers afterwards.

## Debugging regular expressions

Patterns fail quietly: they just match nothing, or too much. A routine that helps:

1. **Collect examples.** Write 3 strings that should match and 3 that should not.
2. **Start small.** Test a tiny piece of the pattern, then add to it.
3. **Print the match.** `print(m.group())` shows what was really caught.
4. **Check the anchors.** A missing `^` or `$` is the most common cause of surprises.
5. **Check the escapes.** A bare `.`, `$`, `(` or `[` is a frequent culprit.
6. **Check greed.** If a match runs on too long, try `*?` or exclude the end character with `[^x]*`.

When a pattern grows past one line, write it in pieces and join them, or add a comment. A regex nobody can read is a bug waiting to happen.

## When not to use regular expressions

Patterns are wonderful for text with a **loose** shape: logs, messy exports, prose. For simple jobs, `str` methods are clearer: `startswith`, `endswith`, `split`, `in`. For structured formats such as HTML, JSON or CSV, use a proper tool for that format (you will meet one for HTML in the networking chapter).

## Common mistakes

- Forgetting to remove the newline before using `$` or comparing lines.
- Dividing by zero when no line matched.
- Treating a loose pattern as a proof of validity.
- Writing one enormous pattern instead of two small steps.
