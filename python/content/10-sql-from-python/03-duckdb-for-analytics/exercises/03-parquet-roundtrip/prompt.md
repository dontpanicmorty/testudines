Write two functions for a small lake step.

`write_parquet(rows, path)` takes a list of dicts with keys `sku` (str), `qty` (int) and `price` (float) and writes them to a Parquet file at `path` (a `str` or `Path`), creating the parent directory if needed. It returns the number of rows written.

`read_parquet_rows(path, min_qty=0)` reads the file back and returns a list of dicts for rows with `qty >= min_qty` (a parameter, not text), ordered by `sku`.

```python
write_parquet([{"sku": "A", "qty": 2, "price": 1.5}], "out/x.parquet")   # 1
read_parquet_rows("out/x.parquet")   # [{"sku": "A", "qty": 2, "price": 1.5}]
```
