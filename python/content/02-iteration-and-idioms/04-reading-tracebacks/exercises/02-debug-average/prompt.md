`average_amount(rows)` should return the mean `amount` across rows, **ignoring** rows whose amount is under the minimum of `0.01` (test fixtures), rounded to 2 decimals. Rows come from a CSV, so `amount` is a **string** like `"12.50"`. For no qualifying rows it returns `0.0`.

Users report: the average is always slightly off, comparisons with the minimum give nonsense for some values, and an empty export crashes the job. Fix the function.

```python
average_amount([{"amount": "10"}, {"amount": "20"}, {"amount": "0"}])   # 15.0
average_amount([])                                                      # 0.0
```
