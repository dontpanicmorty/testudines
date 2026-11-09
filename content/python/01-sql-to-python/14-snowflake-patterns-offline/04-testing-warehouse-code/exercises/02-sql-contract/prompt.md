Write `build_select(table, columns, filters=None)` returning `(sql, params)`.

- `sql` is `SELECT c1, c2 FROM table` and, when filters exist, ` WHERE k1 = %(k1)s AND k2 = %(k2)s` (filter keys in dict order). Whitespace differences are ignored by the tests.
- `params` is a **new** dict equal to `filters` (`{}` when none). Values are never placed in the SQL text.
- Table, column and filter-key names must match `[A-Za-z_][A-Za-z0-9_$]*` (optionally one dotted qualifier for the table, like `raw.orders`); otherwise raise `ValueError`.
- An empty `columns` list raises `ValueError`.

```python
build_select("orders", ["id", "status"], {"region": "EU"})
# ("SELECT id, status FROM orders WHERE region = %(region)s", {"region": "EU"})
```
