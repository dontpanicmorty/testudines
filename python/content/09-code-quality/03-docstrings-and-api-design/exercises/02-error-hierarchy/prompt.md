Design the error API of a tiny CSV loader and implement `load_rows`.

**Exceptions**

- `LoadError(Exception)`: base class for everything the loader raises.
- `SchemaError(LoadError)` has attribute `missing` (sorted list of absent column names); `str(err)` is `"missing columns: amount, id"` (comma-separated, sorted).
- `RowError(LoadError)` has attribute `line_number`; `str(err)` is `"line 3: expected 3 fields, got 2"` (line number, then the message).

**`load_rows(lines, required=("id", "amount"))`**

- The first line is the header (comma-separated; cells stripped). If any required column is missing, raise `SchemaError`. Empty input counts as missing every required column.
- Each later line is split on commas and stripped; blank lines are skipped. If the cell count differs from the header's, raise `RowError(line_number, "expected N fields, got M")`, where line 1 is the header.
- Return a list of dicts, one per row. Extra columns are allowed.

```python
load_rows(["id,amount", "1,5", "2,7"])    # [{'id': '1', 'amount': '5'}, {'id': '2', 'amount': '7'}]
load_rows(["id,amount,note", "1,5"])      # RowError: line 2: expected 3 fields, got 2
```
