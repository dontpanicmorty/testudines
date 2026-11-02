`my_tests.py` tests a small `Cart`. Each test looks right on its own, but when the whole file runs, some tests fail, and run in a different order they fail differently.

Fix the **tests** (not `cart.py`) so that every test passes regardless of order, and keep all four tests.

```python
from cart import Cart
c = Cart()
c.add("A1", 2)
c.count()     # 2
```
