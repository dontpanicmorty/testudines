Write `check_rows(contract, rows)` where `contract` is `{column: type_name}` and `rows` a list of dicts. Return a list of violation tuples `(row_index, column, problem)` sorted by `(row_index, column, problem)`, where `problem` is:

- `"missing"`: the column is absent from the row
- `"wrong_type"`: the value is not `None` and its `type(value).__name__` differs from the contract (an `int` is accepted for a `float` column; a `bool` is **not** accepted for an `int` column)
- `"unexpected"`: the row has a column that is not in the contract

`None` values are always accepted. A clean batch returns `[]`.

```python
check_rows({"id": "int"}, [{"id": "1", "extra": 5}])
# [(0, "extra", "unexpected"), (0, "id", "wrong_type")]
```
