Write `load_rows(rows, parse, reject_path, max_reject_rate=0.2)`.

- Call `parse(raw)` for every raw row. Rows where it raises `ValueError` are rejected; other exceptions propagate.
- Write one JSON line per rejected row to `reject_path`: `{"row": <raw row>, "error": "<message>"}`. Always write the file (empty when nothing was rejected).
- If `len(rejects) / len(rows)` is **greater than** `max_reject_rate`, raise `TooManyRejects` **after** writing the reject file. An empty input is not an error.
- Otherwise return the list of parsed good rows in input order.

```python
good = load_rows(raw_rows, parse_order, "rejects/orders.jsonl", max_reject_rate=0.1)
```
