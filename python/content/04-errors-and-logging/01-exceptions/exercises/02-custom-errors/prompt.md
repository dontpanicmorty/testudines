Define `RowError(Exception)` that carries `row_number` and whose string includes it, e.g. `"row 3: invalid amount 'abc'"`.

Then write `parse_row(row, row_number)` for a dict like `{"id": "7", "amount": "12.5"}` returning `{"id": 7, "amount": 12.5}`. If either conversion fails, raise `RowError` **chained from** the original `ValueError` (so `err.__cause__` is the `ValueError`). A missing key is *not* wrapped: let the `KeyError` escape.

```python
parse_row({"id": "7", "amount": "abc"}, 3)
# RowError: row 3: invalid amount 'abc'
```
