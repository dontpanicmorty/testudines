When a 2-million-row load fails, the first question is "which row, and what error?". Write `first_failure(rows, parse)` from scratch.

`parse` is a function taking one row. Call it on each row in order and stop at the first row that raises any `Exception`. Return `(index, exception_type_name, message)`; if every row parses, return `None`. Rows after the failure must not be passed to `parse`.

```python
first_failure(["1", "2", "x", "4"], int)
# (2, "ValueError", "invalid literal for int() with base 10: 'x'")
first_failure(["1", "2"], int)   # None
```
