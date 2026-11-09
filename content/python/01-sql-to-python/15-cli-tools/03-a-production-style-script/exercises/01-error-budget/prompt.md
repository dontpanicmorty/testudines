Write `evaluate(total, rejected, max_error_rate)` returning `(exit_code, message)`.

- `total == 0`: `(1, "no input rows")`.
- error rate `rejected / total` **greater than** `max_error_rate`: `(1, "error rate 20.0% exceeds budget of 10.0%")`: percentages with one decimal.
- otherwise: `(0, "ok: 5 of 100 rows rejected")`.
- Raise `ValueError` if `rejected > total`, or `rejected < 0`, or `max_error_rate` is outside `0..1`.

```python
evaluate(100, 5, 0.1)    # (0, "ok: 5 of 100 rows rejected")
evaluate(100, 20, 0.1)   # (1, "error rate 20.0% exceeds budget of 10.0%")
```
