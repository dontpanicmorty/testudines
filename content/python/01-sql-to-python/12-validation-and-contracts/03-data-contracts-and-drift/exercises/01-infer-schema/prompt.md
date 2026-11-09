Write `infer_schema(rows)` returning a dict `{column: type_name}` for a list of dict rows. Type names are `type(value).__name__` of the non-`None` values (`"int"`, `"float"`, `"str"`, `"bool"`, ...).

- Columns are in order of first appearance across the rows; a column present in only some rows is still included.
- If a column has only `None` values: `"null"`.
- Mixed `int` and `float` (only those): `"float"`.
- Any other mix: `"str"`.
- No rows: `{}`.

```python
infer_schema([{"id": 1, "x": None}, {"id": 2, "x": None, "y": 2.5}])
# {"id": "int", "x": "null", "y": "float"}
```
