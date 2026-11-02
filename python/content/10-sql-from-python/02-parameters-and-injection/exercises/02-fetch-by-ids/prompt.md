`fetch_by_ids(conn, ids)` returns the rows of `customers(id, name)` whose id is in `ids`, as a list of `(id, name)` tuples ordered by id. It works for two or more ids but **crashes with exactly one id and with an empty list**. It is also building SQL from data, which you should not keep doing. Fix all of it.

```python
fetch_by_ids(conn, [1, 3])   # [(1, 'Ada'), (3, 'Tim')]
fetch_by_ids(conn, [3])      # [(3, 'Tim')]
fetch_by_ids(conn, [])       # []
```
