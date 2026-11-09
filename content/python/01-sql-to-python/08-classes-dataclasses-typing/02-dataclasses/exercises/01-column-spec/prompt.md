A teammate wrote a `ColumnSpec` dataclass for describing warehouse columns, but `import solution` now fails right away. Fix it so the module imports and behaves as follows:

- fields: `name`, `dtype`, `nullable` (default `True`), `tags` (default: a **separate** empty list per instance);
- `describe(col)` returns `"<name>: <dtype>"`, with `" (not null)"` appended when the column isn't nullable.

```python
c = ColumnSpec("order_id", "int", nullable=False, tags=["key"])
describe(c)                    # 'order_id: int (not null)'
describe(ColumnSpec("note", "str"))   # 'note: str'
```
