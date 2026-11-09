Build the pipeline described in the lesson brief across the six files in `pipeline/`. Press **Check** as you go: the test suite is grouped by file, so you can finish and verify one layer at a time.

## Contracts

**`schema.py`**: `validate_orders`, `validate_items`, `validate_customers` each return `(good_rows, quarantined_rows)`.

| Source | Rule (violation quarantines the row; the reason must contain the field name) |
|---|---|
| orders | `order_id`, `customer_id`: positive integers; `placed_at`: `YYYY-MM-DD HH:MM:SS`; `status` (trimmed, lowercased) in `completed, shipped, cancelled, refunded`; a repeated `order_id` is quarantined with a reason containing `duplicate` (first occurrence wins) |
| order_items | `order_id`, `quantity`: positive integers; `product_id`: non-empty; `unit_price`: number >= 0 |
| customers | `customer_id` positive integer (duplicates quarantined, first wins); `region` non-empty, trimmed, lowercased |

Good rows are typed (`int`, `float`) with the keys named in the starter docstrings. Quarantined entries are `{"source", "reason", "raw"}` with `source` of `orders`, `order_items` or `customers`. Missing keys must quarantine the row rather than crash. Never mutate the input rows.

**`transform.py`**: `daily_revenue(orders, items, customers)` returns `{"day", "region", "orders", "revenue"}` rows sorted by `(day, region)`. Only `completed` and `shipped` orders count. `day` is `placed_at[:10]`. `revenue` is the sum of `quantity * unit_price`, rounded to 2 places. An unknown customer gets region `"unknown"`. An order with no items still counts as an order with revenue 0. Items of unknown orders are ignored.

**`load.py`**: `connect` creates the tables (SCHEMA is provided). `load_daily_revenue(conn, rows, replace_all=False)` is atomic and idempotent: by default it replaces **whole days** (delete the days present in `rows`, then insert); with `replace_all=True` it empties the table first. `save_quarantine` is idempotent. `get_watermark` / `set_watermark` store the latest loaded day (`YYYY-MM-DD`) in `pipeline_state` under key `watermark`.

**`run.py`**: `run_pipeline(data_dir, db_path, incremental=False)` reads `orders.csv`, `order_items.csv`, `customers.csv`, validates, quarantines, transforms, loads, and returns

```python
{"orders_read": int, "orders_valid": int, "orders_quarantined": int, "items_quarantined": int,
 "customers_quarantined": int, "rows_loaded": int, "watermark": str | None}
```

- A **full** run rebuilds the table (`replace_all=True`). An **incremental** run, when a watermark exists, only processes orders from the watermark **day onward** (the watermark day itself is reprocessed so late arrivals are caught) and replaces only those days.
- After loading, the watermark becomes the latest loaded day; if no rows were produced it is left alone.
- A missing input file raises `FileNotFoundError` **before** the database is touched or created.
- Log with `logging.getLogger("pipeline")`: INFO for progress, WARNING when rows were quarantined. No `print`.

**`cli.py`**: `main(argv=None) -> int` with `--data-dir` (required), `--db` (required), `--incremental`, `-v/--verbose`. Return `0` on success and `2` (after logging an error) when an input file is missing.

```python
from pipeline.cli import main
main(["--data-dir", "data", "--db", "out.db", "--incremental"])   # 0
```

## Rubric (what the tests look for)

- Correct typing, normalisation and quarantine reasons for every rule above
- Pure transform with correct rounding, filtering and ordering
- Idempotency: running twice changes nothing; failed loads roll back
- Incremental logic: untouched old days, reprocessed watermark day, new days added
- Failure handling: missing files, bad rows, missing keys, no `print` output
- A real run over the bundled `orders`, `order_items` and `customers` data agrees with an independent calculation
