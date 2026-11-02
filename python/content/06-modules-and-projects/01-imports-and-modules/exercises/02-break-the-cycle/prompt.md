Two small modules, `customers.py` and `orders.py`, each import a function from the other at the top. Right now importing **either** module crashes with an `ImportError`.

Change the code so that:

- `import customers` and `import orders` both work, in either order, in a fresh interpreter;
- `customers.order_count(1)` returns `2`;
- `orders.describe_order(102)` returns `"order 102 for Grace"`.

Don't change the data or the public function names.

```python
import orders
print(orders.describe_order(100))   # order 100 for Ada
```
