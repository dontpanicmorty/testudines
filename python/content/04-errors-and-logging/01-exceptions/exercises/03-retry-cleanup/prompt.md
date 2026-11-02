`load_with_retry(load, attempts, on_close)` calls `load()` up to `attempts` times, retrying only when `load` raises `ConnectionError`. If it succeeds, return its result. After the final failed attempt it must raise `ConnectionError("giving up after N attempts")` chained from the last `ConnectionError`. Any other exception type must propagate immediately, with no retry. `on_close()` must be called exactly once at the end, whatever happened.

Right now failures disappear (the function returns `None`), unrelated bugs get retried, and `on_close` is sometimes skipped. Fix it.

```python
load_with_retry(flaky_loader, 3, conn.close)
```
