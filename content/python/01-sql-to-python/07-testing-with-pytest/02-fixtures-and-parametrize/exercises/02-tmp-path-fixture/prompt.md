`customers.active_customers(path)` reads a CSV with the header `customer_id,name,plan` and returns the rows (as dicts of **stripped** strings, in file order) whose plan is **not** `free`. The plan comparison ignores case and surrounding whitespace.

Write tests in `my_tests.py` that:

1. use a `@pytest.fixture` that writes a sample CSV into `tmp_path` and returns its path;
2. pass on the real function and fail on every hidden-bug variant.

```python
from customers import active_customers
rows = active_customers("customers.csv")
# [{'customer_id': '1', 'name': 'Ada', 'plan': 'pro'}, ...]
```

Write at least 3 tests.
