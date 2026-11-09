The nightly job `load_partition(conn, load_date, rows)` loads `(order_id, amount)` pairs into `fact_orders(load_date, order_id, amount)`. After the scheduler retried a run, finance reported that one day's revenue was exactly doubled.

Fix the loader so that:

- running it twice for the same `load_date` leaves exactly one copy of the rows,
- other dates' rows are never touched,
- if inserting fails part-way (for example a bad row), the previously loaded data for that date is still there.

```python
load_partition(conn, "2026-01-01", [(1, 10.0), (2, 5.0)])
load_partition(conn, "2026-01-01", [(1, 10.0), (2, 5.0)])  # no duplicates
```
