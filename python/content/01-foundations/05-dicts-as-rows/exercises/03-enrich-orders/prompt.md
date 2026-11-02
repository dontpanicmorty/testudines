Implement a LEFT JOIN from scratch. Write `enrich_orders(orders, customers)`.

- `orders`: list of dicts with `order_id`, `customer_id`, `amount`.
- `customers`: list of dicts with `customer_id`, `region`, `plan`.
- Return a new list, one dict per order in the original order, containing all the order's fields plus `region` and `plan` from the matching customer. If there is no matching customer, `region` and `plan` are `None`.
- Do not modify the inputs. If `customers` contains the same `customer_id` twice, the **last** one wins.

```python
orders = [{"order_id": 1, "customer_id": "c1", "amount": 9.0},
          {"order_id": 2, "customer_id": "zz", "amount": 5.0}]
customers = [{"customer_id": "c1", "region": "EU", "plan": "pro"}]
enrich_orders(orders, customers)
# [{"order_id": 1, "customer_id": "c1", "amount": 9.0, "region": "EU", "plan": "pro"},
#  {"order_id": 2, "customer_id": "zz", "amount": 5.0, "region": None, "plan": None}]
```
