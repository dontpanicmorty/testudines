+++
id = "capstones.capstone-data-service"
title = "Capstone: a data service"
minutes = 90
+++

# Capstone: a data service

The last capstone puts a front door on your data. The finance team has a `daily_revenue` table and a `customers` table in a DuckDB file, and other teams want to query them without warehouse credentials or SQL. You will build the HTTP service: typed, validated, paginated, observable and safe to retry.

> **SQL bridge.** This is a semantic layer in miniature. Consumers get a stable, documented contract (`/revenue/daily?region=west`) while you stay free to change the tables behind it, hide columns (no `email`) and enforce limits (no `SELECT *` over a billion rows).

## The brief

Implement `revenue_api` with these capabilities:

- **Read endpoints** for daily revenue (list with filters, and one day's detail) and customers (list and single).
- **Validation** of every input: dates, ranges, page numbers, enumerated values.
- **Pagination** with limits that come from configuration.
- **Health endpoint** that reports the real state of the database.
- **Consistent error bodies** for every failure.
- **A write endpoint**, `POST /customers`, made safe to retry with an idempotency key.
- Tests through `TestClient` only. No server is started.

## Architecture

```text
revenue_api/
  settings.py   Settings dataclass, get_settings() (env), get_today()
  db.py         connect(), get_conn() dependency, fetch_all()
  models.py     pydantic request/response models (the public contract)
  errors.py     install_error_handlers(app): one envelope
  app.py        create_app() with the routes
```

`create_app()` is a **factory**: each call builds a new app, so tests get isolated instances and can override dependencies without touching global state.

## Design decisions to think through

**The model is the contract.** The `customers` table contains `email`. Your `Customer` response model does not, and `response_model=Customer` guarantees that no handler can leak it by accident, even if a future query does `select *`:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class PublicCustomer(BaseModel):
    customer_id: int
    first_name: str

app = FastAPI()

@app.get("/customers/1", response_model=PublicCustomer)
def get_customer():
    return {"customer_id": 1, "first_name": "Ada", "email": "ada@example.com"}

print(TestClient(app).get("/customers/1").json())
```

**One connection per request, through a dependency.** DuckDB connections are cheap to open on a local file. A `yield` dependency opens one and closes it in `finally`, and a test can replace the whole dependency:

```python
import duckdb

def fetch_all(conn, sql, params=()):
    cursor = conn.execute(sql, list(params))
    names = [d[0] for d in cursor.description]
    return [dict(zip(names, row)) for row in cursor.fetchall()]

conn = duckdb.connect(":memory:")
conn.execute("create table t(day date, region varchar, revenue double)")
conn.execute("insert into t values ('2025-01-01', 'west', 10.5), ('2025-01-01', 'east', 4.0)")
print(fetch_all(conn, "select region, revenue from t where revenue > ? order by region", [5]))
```

**Shared pagination as a dependency.** Both list endpoints take `page` and `page_size` and apply the same limits. Write that once as a dependency that returns `(page, size)`, reading the default and maximum from injected settings, so tests can run with `max_page_size=4`.

**Rejecting a value with the standard 422.** When validation depends on runtime settings you cannot use `Query(le=...)`. Raise `RequestValidationError` yourself and your envelope handler will format it like every other validation failure:

```python
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def on_validation(request, exc):
    fields = [".".join(str(p) for p in e["loc"]) for e in exc.errors()]
    return JSONResponse({"error": {"code": "validation_error", "fields": fields}}, status_code=422)

@app.get("/items")
def items(page_size: int = 10, max_size: int = 50):
    if page_size > max_size:
        raise RequestValidationError(
            [{"type": "value_error", "loc": ("query", "page_size"), "msg": "too large", "input": page_size}]
        )
    return {"page_size": page_size}

print(TestClient(app).get("/items?page_size=500").json())
```

**Pagination arithmetic.** `has_next = page * size < total`. Always `ORDER BY` a unique column (`customer_id`, or `day, region`), or pages overlap. `total` must count the *filtered* rows, not the page.

**Idempotency that survives restarts.** Keeping seen keys in a Python dict works until a second worker or a restart. Store `(key, fingerprint, response)` in the database and write it in the **same transaction** as the customer: either both exist or neither does. The fingerprint (normalised body) lets you tell a legitimate replay from key reuse with a different payload (`409`). Only record successes; if a rejected request reserved the key, the client's corrected retry would be blocked forever.

**Health must be honest.** A `/health` that returns `ok` without touching the database is a lie. Open a connection and run `select 1`; return `503` when it fails so the load balancer stops sending traffic.

**Never leak internals.** Unexpected exceptions become `500 {"error": {"code": "internal_error", ...}}` with a generic message. Real details belong in logs.

## How to work

1. `settings.py`, `db.py`: small, and everything else depends on them.
2. `errors.py` and `models.py`: the contract and the envelope.
3. `GET /health`, then the read routes one at a time; **Check** after each.
4. The shared pagination dependency, then the filters.
5. `POST /customers` last: validation, duplicates, then the idempotency table and transaction.

## Common mistakes

- **`select *` mapped straight into the response**, leaking columns. Name columns and use `response_model`.
- **Building SQL with f-strings from user input.** Only the *structure* (which `where` clauses exist) may be assembled in code; values go in `?` placeholders.
- **Counting `total` from the page** instead of with a separate `select count(*)`.
- **Forgetting `ORDER BY`**, giving unstable pages.
- **Storing idempotency state in memory** and then losing it on restart or on another worker.
- **Reserving the key before the work succeeds.** Record it inside the success transaction.
- **A `500` that echoes the exception message**, leaking connection strings and table names.

## What to take away

1. The response model is the public contract; hide what consumers must not see.
2. Resources (connections, settings, the clock) come through dependencies so tests can swap them.
3. Paginate with a stable order, a bounded size from config, and an honest `total` and `has_next`.
4. One error envelope for every failure, with no internals in it.
5. Idempotency keys live in the database, are written atomically with the work, and are recorded only on success.
6. Health checks must exercise the real dependency.
