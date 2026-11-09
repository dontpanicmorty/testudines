Implement `is_transient(exc)`. It returns `True` when retrying might help:

- `ConnectionError` and `TimeoutError` (and subclasses)
- `HttpError` with status 429 or any status >= 500

Everything else, including `HttpError` 400/401/403/404 and `ValueError`, returns `False`.

```python
is_transient(HttpError(503))   # True
is_transient(HttpError(404))   # False
is_transient(ValueError("x"))  # False
```
