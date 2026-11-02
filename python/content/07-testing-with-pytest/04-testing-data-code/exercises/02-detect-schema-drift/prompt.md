Implement `check_schema(expected, actual)` for a loader's contract test. Both arguments map column names to type names (strings). Return a **list of problem messages**, empty when the schemas match. For each column in either schema, sorted by column name, add at most one message:

- `"missing column: <name>"`: in `expected` but not in `actual`;
- `"unexpected column: <name>"`: in `actual` but not in `expected`;
- `"type changed: <name> <expected_type> -> <actual_type>"`: in both with different types.

```python
expected = {"order_id": "int", "total": "float"}
actual = {"order_id": "str", "region": "str"}
check_schema(expected, actual)
# ['type changed: order_id int -> str', 'unexpected column: region', 'missing column: total']
```
