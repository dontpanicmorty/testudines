Write `classify_order(row)` from scratch. `row` is a dict like `{"status": "Shipped ", "amount": 50.0}` or `None`.

Return one of these strings, using the first rule that applies:

1. `"invalid"` if `row` is `None`, or has no `status` key, or `status` is not a string.
2. `"closed"` if the status (stripped, lowercased) is `cancelled` or `returned`.
3. `"unpaid"` if `amount` is missing, `None`, or `<= 0`.
4. `"fulfilled"` if status is `shipped` or `delivered`.
5. `"open"` otherwise.

```python
classify_order({"status": "Shipped ", "amount": 50})  # "fulfilled"
classify_order({"status": "pending", "amount": 50})   # "open"
classify_order({"status": "shipped"})                 # "unpaid"
classify_order({"status": "RETURNED", "amount": 5})   # "closed"
classify_order(None)                                  # "invalid"
```
