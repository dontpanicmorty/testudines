Warehouses load many mid-sized files faster than one huge one. Write `write_chunks(rows, out_dir, prefix, max_rows, fieldnames)`:

- `rows` is an iterable of dicts (it may be a generator; stream it, don't build a list).
- Write CSV files into `out_dir` (a `pathlib.Path`, already existing) named `{prefix}_0001.csv`, `{prefix}_0002.csv`, ... Each file has a header row (`fieldnames`) and at most `max_rows` data rows.
- Return the list of `Path`s created, in order. No rows means no files and `[]`.
- `max_rows < 1` raises `ValueError`.

```python
paths = write_chunks(({"id": i} for i in range(5)), out, "orders", 2, ["id"])
[p.name for p in paths]   # ["orders_0001.csv", "orders_0002.csv", "orders_0003.csv"]
```
