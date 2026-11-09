A customers export must be shared per region. Write `split_by_region(src, out_dir)`:

- Read `src` (CSV with a `region` column and any other columns).
- Create `out_dir` if needed and write one file per region named `<region>.csv`, each with the **same header and column order** as the source.
- Rows keep their original relative order.
- Return a dict `{region: row_count}`.

```python
split_by_region(Path("customers.csv"), Path("out"))   # {"EU": 2, "US": 1}
```
