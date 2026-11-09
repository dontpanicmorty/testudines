Write `check_orders(rows)` returning a list of problem codes (strings). An empty list means the data passed. Use exactly these codes, each at most once, in this order when several apply:

1. `"empty"`: there are no rows (return just this, nothing else).
2. `"null_order_id"`: any row has `order_id` missing or `None`.
3. `"duplicate_order_id"`: any non-null `order_id` appears more than once.
4. `"bad_amount"`: any row where `amount` is missing, `None`, not a number, or negative.

The function must never raise because of bad data.

```python
check_orders([{"order_id": 1, "amount": 5.0}, {"order_id": 1, "amount": -1}])
# ["duplicate_order_id", "bad_amount"]
```
