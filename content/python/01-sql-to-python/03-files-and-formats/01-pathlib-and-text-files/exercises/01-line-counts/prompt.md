A vendor drops a text export with blank spacer lines. Write `count_records(path)` that returns how many **non-blank** lines the file contains (a line with only spaces counts as blank). Stream the file; do not assume it is small.

```python
# file content: "a\n\n  \nb\nc\n"
count_records(Path("export.txt"))   # 3
```
