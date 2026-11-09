Write `run_step(rows, transform, run_id, max_failures=2)` with a module-level logger named `__name__`.

For each row (1-based index `n`) call `transform(row)`:

- On success, collect the result.
- If it raises `ValueError`, log at WARNING `run=<run_id> row=<n> skipped: <error>` and continue.
- After the loop, log at INFO `run=<run_id> ok=<k> skipped=<s>` and return the list of results.
- If skipped count is greater than `max_failures`, log at ERROR `run=<run_id> too many failures skipped=<s>` and raise `RuntimeError` instead of returning (the INFO summary is not logged in that case).

```python
run_step(["1", "x", "3"], int, "r1")   # [1, 3]  (logs one warning, one info)
```
