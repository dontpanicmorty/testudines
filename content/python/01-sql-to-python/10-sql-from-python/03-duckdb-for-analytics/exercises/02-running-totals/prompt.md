Given a list of ledger entries `(account, day, amount)` (day is an ISO string like `"2025-01-31"`), return `(account, day, amount, running_total)` tuples where `running_total` is the cumulative sum of `amount` **within each account** in date order. Do the computation with a DuckDB window function. Output is ordered by account, then day; `day` stays a string in the result.

```python
running_totals([("a", "2025-01-01", 10), ("a", "2025-01-02", -4), ("b", "2025-01-01", 7)])
# [("a", "2025-01-01", 10, 10), ("a", "2025-01-02", -4, 6), ("b", "2025-01-01", 7, 7)]
```
