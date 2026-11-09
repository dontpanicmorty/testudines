Incremental loads track a **watermark**: the newest timestamp already processed. Write the class `Watermark` (timestamps are ISO-8601 strings, which sort correctly as text).

- `Watermark(start=None)` begins at `start`. The current value is the attribute `value` (`None` means nothing processed yet).
- `is_new(ts)` is `True` if `ts` is newer than the watermark (always `True` when the value is `None`).
- `advance(ts)` moves the watermark to `ts` **only if** `ts` is newer; it returns `True` if it moved and `False` otherwise. The watermark never goes backwards.
- `repr` looks like `Watermark('2025-01-05')` or `Watermark(None)`.

```python
w = Watermark()
w.advance("2025-01-05")   # True
w.advance("2025-01-03")   # False  (late arrival, ignored)
w.value                   # '2025-01-05'
w.is_new("2025-01-06")    # True
print(w)                  # Watermark('2025-01-05')
```
