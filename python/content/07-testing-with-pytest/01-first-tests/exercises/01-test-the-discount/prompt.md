`pricing.py` contains `apply_discount(price, percent)`. Its contract:

- returns `price` reduced by `percent` percent, **rounded to 2 decimals**;
- `percent` must be between 0 and 100 **inclusive**, otherwise it raises `ValueError`.

You write the tests, in `my_tests.py`. Your tests will be run against the real function (they must pass) and against several versions with a hidden bug each (your tests must fail on every one). Think about what could go wrong in each line of the contract.

```python
from pricing import apply_discount
apply_discount(200, 25)    # 150.0
apply_discount(10, 33.33)  # 6.67
apply_discount(10, 101)    # raises ValueError
```

Use plain `assert` and `pytest.raises`. Aim for at least 5 test cases.
