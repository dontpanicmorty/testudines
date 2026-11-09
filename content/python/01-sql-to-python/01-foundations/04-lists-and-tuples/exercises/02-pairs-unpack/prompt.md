A tiny export arrives as a list of text lines; the first line is the header.

Write `split_export(lines)` returning a tuple `(columns, rows)`:

- `columns`: list of header names, stripped and lowercased
- `rows`: list of **tuples**, one per remaining line, with every cell stripped
- Blank lines (empty or whitespace only) are skipped.

```python
lines = ["ID, Name ,Plan", "1, Ada ,pro", "", "2,Grace,free"]
split_export(lines)
# (["id", "name", "plan"], [("1", "Ada", "pro"), ("2", "Grace", "free")])
```
