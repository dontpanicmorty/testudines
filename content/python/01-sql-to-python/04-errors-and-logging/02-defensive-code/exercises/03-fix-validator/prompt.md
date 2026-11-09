`clean_orders(rows, seen_ids=None)` is meant to return validated order dicts and to drop **repeated `order_id`s** within one call (first one wins). Invalid rows must raise `ValueError` (not `AssertionError`).

Observed problems: invalid rows produce `AssertionError` (and would pass entirely in an optimised run), a second call to `clean_orders` wrongly drops ids that only appeared in the *first* call, and a missing status turns into the text `"None"`.

Rules: `order_id` non-empty string, `quantity` a positive int (given as text), `status` one of `paid`, `open`, `void` (case-insensitive, returned lowercase). Rows are dicts.

```python
clean_orders([{"order_id": "A", "quantity": "2", "status": "Paid"}])
# [{"order_id": "A", "quantity": 2, "status": "paid"}]
```
