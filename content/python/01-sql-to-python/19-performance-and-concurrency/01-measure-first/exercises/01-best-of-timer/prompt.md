Write `best_of(fn, number=1000, repeat=5, timer=time.perf_counter)` that benchmarks a zero-argument function.

It performs `repeat` runs. In each run it reads `timer()`, calls `fn()` exactly `number` times, reads `timer()` again. It returns the **smallest** run duration divided by `number` (seconds per call).

The `timer` parameter exists so tests can pass a fake clock; always use it rather than calling `time.perf_counter` directly.

```python
best_of(lambda: sum(range(100)), number=500, repeat=3)   # e.g. 1.2e-06
```

Raise `ValueError` if `number` or `repeat` is less than 1.
