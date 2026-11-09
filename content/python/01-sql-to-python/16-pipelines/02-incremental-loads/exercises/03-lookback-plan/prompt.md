Late-arriving rows are being missed. Write `plan_incremental(source_rows, watermark, lookback_hours)` that returns the rows to upsert this run.

- If `watermark` is `None`, consider every row.
- Otherwise consider rows whose `updated_at` is **at or after** `watermark - lookback_hours`.
- If an `id` appears more than once among the considered rows, keep only the version with the greatest `updated_at`.
- Return the result sorted by `id`.

Timestamps are ISO-8601 strings like `"2026-01-02T08:15:00"`.

```python
rows = [{"id": 1, "updated_at": "2026-01-02T05:00:00"},
        {"id": 2, "updated_at": "2026-01-02T07:30:00"}]
plan_incremental(rows, "2026-01-02T08:00:00", 1)   # only id 2 (07:30 >= 07:00)
```
