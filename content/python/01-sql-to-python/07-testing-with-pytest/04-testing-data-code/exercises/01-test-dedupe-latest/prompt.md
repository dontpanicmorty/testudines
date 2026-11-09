`dedupe.dedupe_latest(rows)` keeps one row per `"id"` from a change feed:

- the winner is the row with the greatest `"updated_at"` (ISO-8601 strings, so string comparison works);
- `None` counts as **older** than any timestamp;
- on an exact tie, the **later** row in the input wins;
- the result is sorted by `"id"`;
- the input list and its rows are **not modified**.

Write `my_tests.py` with small inline fixtures. It must pass on the real function and catch every hidden-bug variant.

```python
from dedupe import dedupe_latest
rows = [
    {"id": 2, "updated_at": "2025-01-02", "v": "old"},
    {"id": 1, "updated_at": "2025-01-01", "v": "a"},
    {"id": 2, "updated_at": "2025-01-05", "v": "new"},
]
dedupe_latest(rows)   # id 1 row, then the id 2 row with v == "new"
```

Write at least 5 tests.
