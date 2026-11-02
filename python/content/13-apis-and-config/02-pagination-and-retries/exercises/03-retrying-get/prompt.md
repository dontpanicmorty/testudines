Write `get_with_retries(client, path, max_attempts=4, sleep=time.sleep)` that returns the parsed JSON of a successful `GET`.

Rules:

- Retry on transport errors (`httpx.TransportError`, e.g. timeouts), on `429`, and on any `5xx`.
- Wait before each retry by calling `sleep(seconds)`. Normally `0.5 * 2**attempt` (attempt starts at 0: 0.5, 1.0, 2.0...). For a `429` that has a `Retry-After` header (whole seconds), sleep that many seconds instead.
- Any other non-2xx (400, 401, 404...) is **not** retried: raise `httpx.HTTPStatusError` immediately.
- After `max_attempts` failed tries, raise `RetryExhausted` (already defined). Never sleep after the last attempt.

```python
slept = []
get_with_retries(client, "/report", sleep=slept.append)   # server said 503, 429(Retry-After: 3), then 200
slept                                                      # [0.5, 3.0]
```
