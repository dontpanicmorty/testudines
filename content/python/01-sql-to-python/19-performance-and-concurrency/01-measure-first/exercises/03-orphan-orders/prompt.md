Data quality check: find orders that reference customers that do not exist (a left anti-join).

Write `orphan_order_ids(orders, customers)`.

- `orders`: list of dicts with `order_id` and `customer_id`
- `customers`: list of dicts with `customer_id`
- Return the **sorted list of unique `order_id`s** whose `customer_id` is not present in `customers`. Orders with `customer_id` of `None` count as orphans.

```python
orphan_order_ids(
    [{"order_id": 3, "customer_id": 9}, {"order_id": 1, "customer_id": 1}, {"order_id": 3, "customer_id": 9}],
    [{"customer_id": 1}],
)   # [3]
```

It will be run on 200,000 orders against 100,000 customers and must finish in well under a second.
