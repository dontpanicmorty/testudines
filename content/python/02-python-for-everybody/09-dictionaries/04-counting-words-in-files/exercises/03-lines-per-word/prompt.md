Write `line_spread(path)` that reads a text file and returns a dictionary mapping each word to **the number of lines it appears on** (not the number of times it appears). Ignore capitalization and punctuation (remove every punctuation character, so `"it's"` becomes `"its"`). A word used three times on one line still counts as 1 for that line. Blank lines add nothing.

```
the cat and the hat
a cat
```

gives `{"the": 1, "cat": 2, "and": 1, "hat": 1, "a": 1}`.
