Write `retry(fn, attempts, is_retryable, base_delay=1.0, sleep=time.sleep)`.

- Call `fn()` and return its result on success.
- If it raises an exception for which `is_retryable(exc)` is true and attempts remain, call `sleep(delay)` and try again. The delay doubles each time: `base_delay`, `2*base_delay`, `4*base_delay`, ...
- A non-retryable exception is raised immediately without sleeping.
- When attempts run out, raise the **last** exception. No sleep after the final attempt.

```python
waits = []
retry(flaky_call, attempts=4, is_retryable=is_transient, base_delay=0.5, sleep=waits.append)
# if it failed twice then succeeded: waits == [0.5, 1.0]
```
