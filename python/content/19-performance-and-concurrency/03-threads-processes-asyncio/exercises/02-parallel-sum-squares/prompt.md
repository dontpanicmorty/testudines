Write `sum_of_squares(numbers, workers=2)` returning the sum of `n * n` for every integer in `numbers`, computed by splitting the list across a **`ProcessPoolExecutor`** with `workers` processes.

- Result must equal `sum(n * n for n in numbers)` exactly (integers, so no rounding issues).
- Works for an empty list (returns `0`) and for fewer numbers than workers.
- `workers < 1` raises `ValueError`.
- The function run in the worker processes must be defined at module top level.

```python
sum_of_squares([1, 2, 3, 4], workers=2)   # 30
```
