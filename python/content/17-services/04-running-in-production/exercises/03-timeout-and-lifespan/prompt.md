Write `create_app(fetch, events, timeout)`:

- `fetch` is an `async` function taking no arguments and returning a string (a stand-in for a slow warehouse call).
- `events` is a list the app appends to: `"startup"` when the app starts and `"shutdown"` when it stops (use a FastAPI lifespan).
- `GET /report` awaits `fetch()` for at most `timeout` seconds. On success it returns `{"report": <value>}`. On timeout it returns `504` with `{"detail": "upstream timed out"}`.
- If `fetch` raises any other exception, return `502` with `{"detail": "upstream failed"}`.
- `GET /health` returns `{"status": "ok"}` and never calls `fetch`.

```python
events = []
app = create_app(fetch, events, timeout=0.05)
with TestClient(app) as client:      # runs startup and shutdown
    client.get("/report")
print(events)                        # ['startup', 'shutdown']
```
