`add_region(orders, customers)` attaches each customer's `region` to their orders. Orders whose customer does not exist are dropped, and output order follows `orders`.

```python
customers = [{"customer_id": 1, "region": "west"}]
orders = [{"order_id": 10, "customer_id": 1}, {"order_id": 11, "customer_id": 99}]
add_region(orders, customers)   # [{"order_id": 10, "customer_id": 1, "region": "west"}]
```

The results are correct, but on a realistic export (thousands of customers and orders) the function takes seconds and gets dramatically worse as the data grows. Make it fast without changing results.
