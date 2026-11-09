+++
id = "services.service-patterns-for-data"
title = "Service patterns for data"
minutes = 30
+++

# Service patterns for data

A data service is usually a *thin read layer* over tables you already trust: an analyst, a dashboard or another team's code asks "give me orders for customer 42" and you answer from the warehouse. The hard part is not the SQL; it is the habits that keep the service predictable under real use: pagination, health checks, configuration, consistent errors, and safe retries for writes.

> **SQL bridge.** A paginated endpoint is `LIMIT/OFFSET` over HTTP. A health check is `SELECT 1`. An idempotency key is `MERGE ... ON key`: apply a change once, no matter how many times it is submitted.

## One connection per request, via a dependency

Open the database in a dependency and close it afterwards. A dependency written with `yield` runs its cleanup after the response is sent.

```python
import sqlite3
import tempfile
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

db_path = Path(tempfile.mkdtemp()) / "shop.db"
setup = sqlite3.connect(db_path)
setup.execute("create table orders(order_id int, customer_id int, total real)")
setup.executemany("insert into orders values (?,?,?)", [(i, i % 3, i * 10.0) for i in range(1, 8)])
setup.commit()
setup.close()

def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

app = FastAPI()

@app.get("/orders/count")
def count(db: sqlite3.Connection = Depends(get_db)) -> dict:
    return {"count": db.execute("select count(*) from orders").fetchone()[0]}

print(TestClient(app).get("/orders/count").json())
```

Always use **parameter placeholders** (`?`) for values; never build SQL with f-strings from request input.

## Pagination

Never return an unbounded table. Accept `page` and `page_size`, bound them, and tell the caller how much exists.

```python
def page_query(db, page: int, page_size: int) -> dict:
    total = db.execute("select count(*) from orders").fetchone()[0]
    rows = db.execute(
        "select * from orders order by order_id limit ? offset ?",
        (page_size, (page - 1) * page_size),
    ).fetchall()
    return {
        "items": [dict(r) for r in rows],
        "page": page,
        "page_size": page_size,
        "total": total,
        "has_next": page * page_size < total,
    }

import sqlite3
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute("create table orders(order_id int, total real)")
conn.executemany("insert into orders values (?,?)", [(i, i * 1.5) for i in range(1, 8)])
out = page_query(conn, page=2, page_size=3)
print([r["order_id"] for r in out["items"]], out["has_next"])
```

The `order by` is not optional: without a stable order, pages overlap or skip rows, exactly as in SQL.

## Health checks

Orchestrators need to ask "are you alive?" and "can you do work?". Keep them cheap and honest: report dependency status, and answer `503` when the service cannot serve.

```python
import sqlite3
from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI()
state = {"db": sqlite3.connect(":memory:")}

@app.get("/health")
def health(response: Response) -> dict:
    try:
        state["db"].execute("select 1")
        return {"status": "ok", "database": "up"}
    except sqlite3.Error:
        response.status_code = 503
        return {"status": "degraded", "database": "down"}

client = TestClient(app)
print(client.get("/health").json())
state["db"].close()
r = client.get("/health")
print(r.status_code, r.json())
```

## Configuration through dependencies

Read settings in **one place**, as a dependency, so tests can override them. Never read environment variables deep inside handlers.

```python
import os
from dataclasses import dataclass

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

@dataclass(frozen=True)
class Settings:
    max_page_size: int = 100
    environment: str = "dev"

def get_settings() -> Settings:
    return Settings(
        max_page_size=int(os.environ.get("MAX_PAGE_SIZE", "100")),
        environment=os.environ.get("APP_ENV", "dev"),
    )

app = FastAPI()

@app.get("/config")
def show(settings: Settings = Depends(get_settings)) -> dict:
    return {"max_page_size": settings.max_page_size, "env": settings.environment}

client = TestClient(app)
print(client.get("/config").json())
app.dependency_overrides[get_settings] = lambda: Settings(max_page_size=5, environment="test")
print(client.get("/config").json())
```

## Consistent error bodies

By default FastAPI answers a 404 with `{"detail": "..."}` and a 422 with a `detail` *list*. Two shapes means every client needs two parsers. Pick **one envelope** and install handlers that apply it everywhere:

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()

def error(status: int, code: str, message: str, **extra) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message, **extra}})

@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return error(exc.status_code, "http_error", str(exc.detail))

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    fields = [".".join(str(p) for p in e["loc"]) for e in exc.errors()]
    return error(422, "validation_error", "invalid request", fields=fields)

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    raise HTTPException(404, f"order {order_id} not found")

client = TestClient(app)
print(client.get("/orders/5").json())
print(client.get("/orders/abc").json())
```

Unexpected exceptions (real bugs) should become a generic `500` envelope that does **not** leak the traceback, while the details go to your logs.

## Idempotency keys for POST

Networks retry. A client that never saw your `201` will send the POST again, and without protection you create two payments. The standard fix: the client sends an `Idempotency-Key` header; you remember the response for that key.

```python
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()
payments: list[dict] = []
seen: dict[str, dict] = {}

@app.post("/payments", status_code=201)
def create_payment(body: dict, idempotency_key: str = Header()):
    if idempotency_key in seen:
        return JSONResponse(seen[idempotency_key], status_code=201)
    payment = {"payment_id": len(payments) + 1, "amount": body["amount"]}
    payments.append(payment)
    seen[idempotency_key] = payment
    return payment

c = TestClient(app)
a = c.post("/payments", json={"amount": 50}, headers={"Idempotency-Key": "abc"})
b = c.post("/payments", json={"amount": 50}, headers={"Idempotency-Key": "abc"})
print(a.json() == b.json(), len(payments))
```

Two retries, one payment. A complete version also rejects the same key reused with a *different* body (`409`), because that is a client bug you should surface, not hide.

## Common mistakes

- **No `order by` with `limit/offset`.** Rows repeat or vanish between pages.
- **Unbounded `page_size`.** One caller asks for a million rows. Cap it with `Query(le=...)`.
- **Sharing one sqlite connection across requests.** You will meet `ProgrammingError: SQLite objects created in a thread can only be used in that same thread`. Use a connection per request.
- **Health check that always says ok.** If it never touches the dependency it cannot detect an outage.
- **Idempotency store that records the key before the work succeeds.** A failed attempt then blocks the retry. Record only after success.

## What to take away

1. Open resources in a `yield` dependency; clean up in `finally`.
2. Paginate with a bounded `page_size`, a stable `order by`, and a `total`/`has_next`.
3. A health check must exercise a real dependency and return `503` when it fails.
4. Centralise settings in one dependency so tests can override them.
5. One error envelope for every failure, with no internals leaked.
6. Make writes safe to retry with idempotency keys.
