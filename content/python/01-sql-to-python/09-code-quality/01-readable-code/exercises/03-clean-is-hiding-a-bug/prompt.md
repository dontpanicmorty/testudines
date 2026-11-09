`clean(o)` is supposed to drop cancelled orders and orders whose total is zero or negative, keeping the rest in their original order. Reports built from it sometimes still contain bad orders, and callers have noticed their original list is changed too.

Fix the behaviour, and while you're in there make the code readable: **the parameter must have a descriptive name** (not a single letter). Keep the function name `clean`.

```python
orders = [
    {"status": "cancelled", "total": 10},
    {"status": "cancelled", "total": 20},
    {"status": "paid", "total": 30},
]
clean(orders)   # [{'status': 'paid', 'total': 30}]
orders          # unchanged, still 3 orders
```
