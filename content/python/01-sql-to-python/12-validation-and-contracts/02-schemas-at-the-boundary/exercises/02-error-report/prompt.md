Given rejects shaped like `{"index": 4, "row": {...}, "errors": [{"field": "amount", "message": "..."}]}`, write `error_report(rejects, total_rows)` returning a dict:

- `rejected`: number of reject records
- `reject_rate`: `rejected / total_rows` rounded to 4 decimals (`0.0` if `total_rows` is 0)
- `by_field`: a list of `{"field": name, "error_count": n, "rows_affected": m}` where `error_count` counts every error on that field and `rows_affected` counts distinct reject records having at least one error on it; sorted by `error_count` descending then `field` ascending
- `sample_indexes`: the first 3 reject indexes, in order

```python
error_report([], 10)   # {"rejected": 0, "reject_rate": 0.0, "by_field": [], "sample_indexes": []}
```
