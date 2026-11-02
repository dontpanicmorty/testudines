`read_valid` and `customer_totals` are already written for you. Implement `run_etl(src, db_path, reject_path)`:

1. `read_valid(src)` gives `(valid, rejects)`.
2. Rows repeated by `(order_id, sku)` within the file: the **last** one wins.
3. Load into the sqlite database at `db_path`:
   - `order_lines(order_id TEXT, sku TEXT, customer_id INTEGER, quantity INTEGER, unit_price TEXT, PRIMARY KEY (order_id, sku))`
   - `customer_totals(customer_id INTEGER PRIMARY KEY, line_count INTEGER, revenue TEXT)` rebuilt from the deduplicated rows using `customer_totals`.
   `unit_price` and `revenue` are stored as text such as `"5.00"`. Running the ETL again on the same file must leave the tables unchanged (idempotent). Write everything in one transaction and close the connection.
4. Write `reject_path` as a CSV with header `line,reason` and one row per reject (header only if none).
5. Return `{"read": <data rows in file>, "loaded": <deduplicated valid rows>, "rejected": <count>}`.

```python
run_etl(Path("lines.csv"), Path("wh.db"), Path("rejects.csv"))
# {"read": 5, "loaded": 3, "rejected": 2}
```
