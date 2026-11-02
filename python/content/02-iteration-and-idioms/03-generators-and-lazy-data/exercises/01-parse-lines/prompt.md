Write a **generator function** `parse_lines(lines)` that takes any iterable of text lines like `"o1,19.99"` and lazily yields `(order_id, amount)` tuples with `amount` as a float.

- Skip lines that are blank (after stripping) or start with `#`.
- Strip whitespace around each field.
- It must be lazy: it must not read more lines than needed.

```python
list(parse_lines(["o1, 19.99", "", "# comment", "o2,5"]))
# [("o1", 19.99), ("o2", 5.0)]
```
