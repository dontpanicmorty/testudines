Write `select_new(rows, watermark)` returning `(new_rows, next_watermark)`.

- `new_rows`: rows whose `updated_at` (ISO string) is strictly greater than `watermark`, sorted by `updated_at` ascending. If `watermark` is `None`, every row is new.
- `next_watermark`: the largest `updated_at` among the new rows, or the unchanged `watermark` when there are none.

```python
rows = [{"id": 1, "updated_at": "2026-01-01T09:00:00"},
        {"id": 2, "updated_at": "2026-01-02T08:00:00"}]
select_new(rows, "2026-01-01T09:00:00")
# ([{"id": 2, "updated_at": "2026-01-02T08:00:00"}], "2026-01-02T08:00:00")
```
