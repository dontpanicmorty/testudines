A rowing club logs sessions as text, one `name,minutes` pair per line:

```
asha,30
ben,45
asha,25
```

Write `report(text)` that returns a multi-line string with each person's total, largest total first (ties broken alphabetically by name), in the form `name: minutes`, lines joined with `"\n"` and no trailing newline. Ignore blank lines. An empty log gives an empty string.

```python
report("asha,30\nben,45\nasha,25")   # "asha: 55\nben: 45"
```

Structure your solution as small functions, one for each stage of input, processing and output.
