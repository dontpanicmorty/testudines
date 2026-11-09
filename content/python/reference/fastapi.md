# FastAPI cheat sheet

| Need | Code |
|---|---|
| App | `app = FastAPI()` |
| Read route | `@app.get("/orders/{order_id}")` |
| Create route | `@app.post("/orders", status_code=201)` |
| Path param | `def f(order_id: int)` (name appears in the path) |
| Query param | `def f(limit: int = 10)` (any other argument) |
| Bounded query | `limit: Annotated[int, Query(ge=1, le=100)] = 10` |
| Header | `key: str = Header()` (`Idempotency-Key` becomes `idempotency_key`) |
| JSON body | `def f(body: OrderIn)` with a pydantic model |
| Output contract | `@app.get(..., response_model=OrderOut)` |
| Raise an error | `raise HTTPException(status_code=404, detail="...")` |
| Dependency | `def f(db = Depends(get_db))` |
| Cleanup after request | `def get_db(): ...; try: yield conn; finally: conn.close()` |
| Startup/shutdown | `FastAPI(lifespan=lifespan)` with an `@asynccontextmanager` |
| Middleware | `@app.middleware("http")` then `await call_next(request)` |

## Status codes

| Code | Use |
|---|---|
| 200 | read ok |
| 201 | created |
| 204 | ok, no body |
| 400 | malformed |
| 401 / 403 | not authenticated / not allowed |
| 404 | not found |
| 409 | conflict (duplicate, key reuse) |
| 422 | validation failed |
| 500 / 502 / 503 / 504 | our bug / upstream bad / unavailable / upstream timeout |

## Testing

```python
from fastapi.testclient import TestClient

client = TestClient(app)                       # no server, no ports
r = client.get("/orders", params={"limit": 5})
r = client.post("/orders", json={"customer_id": 1}, headers={"X-Request-ID": "a"})
r.status_code, r.json(), r.headers["x-request-id"]

app.dependency_overrides[get_db] = lambda: fake_db   # swap a dependency
app.dependency_overrides.clear()

with TestClient(app) as client:                # runs lifespan startup and shutdown
    ...
```

## 422 body shape

```python
{"detail": [{"type": "int_parsing", "loc": ["query", "limit"], "msg": "...", "input": "abc"}]}
```

## Habits

- One error envelope for every failure; never return exception text on a 500.
- Pagination: bounded `page_size`, stable `ORDER BY`, return `total`.
- Per-request connection through a `yield` dependency; settings through a dependency.
- Workers share nothing: shared state belongs in a database.
- A timeout on every outbound call; map it to `504`.
