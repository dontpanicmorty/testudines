`python -m mypy --strict solution.py` reports three errors in `solution.py`. Each one is a real bug: a promise in a signature that the body doesn't keep. Fix the code so that mypy is clean **and** the functions behave as described:

- `find_email(customer_id)` returns the customer's email, or `None` for an unknown id;
- `average_age(ages)` returns the exact average as a float (`average_age([20, 25]) == 22.5`);
- `total_rows(counts)` sums a list of integers.

You may not use `# type: ignore`, `cast` or `Any`.

```python
find_email("c1")        # 'ada@example.com'
find_email("zzz")       # None
```
