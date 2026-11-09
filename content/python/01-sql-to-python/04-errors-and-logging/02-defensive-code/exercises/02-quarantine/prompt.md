Write `process(rows, validate, max_reject_rate=0.05)`.

- Call `validate(raw)` for each row (it raises `ValueError` for bad rows).
- Return `(good, rejected)`. `good` holds the validated outputs in order. Each `rejected` item is `{"row": <1-based position>, "reason": <str of the error>, "raw": <the original row>}`.
- If `len(rejected) / len(rows)` is **greater than** `max_reject_rate`, raise `TooManyRejects` (already defined) instead of returning. An empty input returns `([], [])`.
- Errors other than `ValueError` must not be caught.

```python
good, rejected = process(rows, validate)
```
