`read_order_lines(path)` reads a CSV with columns `order_id,product_id,quantity,unit_price` and returns a **list of dicts** with `order_id` and `quantity` as `int`, `unit_price` as `float`, and `product_id` left as `str`.

```python
# file: order_id,product_id,quantity,unit_price
#       1,P-7,3,4.5
read_order_lines(path)   # [{"order_id": 1, "product_id": "P-7", "quantity": 3, "unit_price": 4.5}]
```
