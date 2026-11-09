+++
id = "services.fastapi-basics"
title = "FastAPI basics"
minutes = 30
+++

# FastAPI basics

FastAPI is a thin layer that does three jobs for you: **routing** (which function handles which URL), **validation** (is the input the right shape?), and **documentation** (it generates a machine-readable description of your API). You write ordinary functions with type hints; the hints *are* the contract.

> **SQL bridge.** Think of a route's type hints as a table's column types and constraints. Bad input is rejected at the door, the same way `INSERT` rejects a string in an INTEGER column, except here the rejection is a clean `422` response.

Everything in this lesson is tested in-process with `TestClient`. It calls your app directly, so **no server is ever started** and tests are fast and deterministic.

## Your first route

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

client = TestClient(app)
response = client.get("/health")
print(response.status_code, response.json())
```

The decorator registers the function for `GET /health`. Returned dicts are serialised to JSON for you.

## Path and query parameters

A name in the path braces is a **path parameter**. Any other function argument is a **query parameter** (`?limit=5`). The type hint converts and validates.

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/orders/{order_id}")
def get_order(order_id: int, verbose: bool = False) -> dict:
    return {"order_id": order_id, "verbose": verbose}

client = TestClient(app)
print(client.get("/orders/5?verbose=true").json())
bad = client.get("/orders/abc")
print(bad.status_code)
print(bad.json()["detail"][0]["loc"], bad.json()["detail"][0]["msg"])
```

> **Predict first.** `/orders/abc` never reaches your function. What status does the caller get, and who produced the error body?

FastAPI answered **422 Unprocessable Entity** before calling your code. The body's `detail` is a list of problems, each with a `loc` (where: `["path", "order_id"]`) and a `msg`.

Add limits with `Query`:

```python
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/orders")
def list_orders(limit: Annotated[int, Query(ge=1, le=100)] = 10) -> dict:
    return {"limit": limit}

client = TestClient(app)
print(client.get("/orders").json())
print(client.get("/orders?limit=500").status_code)
```

## Request bodies with pydantic

For a POST, declare a pydantic model as a parameter. FastAPI parses the JSON body, validates it, and hands you a real object.

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

class ItemIn(BaseModel):
    sku: str
    quantity: int = Field(gt=0)

class OrderIn(BaseModel):
    customer_id: int
    items: list[ItemIn] = Field(min_length=1)

app = FastAPI()

@app.post("/orders", status_code=201)
def create_order(order: OrderIn) -> dict:
    return {"customer_id": order.customer_id, "lines": len(order.items)}

client = TestClient(app)
ok = client.post("/orders", json={"customer_id": 7, "items": [{"sku": "P003", "quantity": 2}]})
print(ok.status_code, ok.json())
bad = client.post("/orders", json={"customer_id": 7, "items": [{"sku": "P003", "quantity": 0}]})
print(bad.status_code, bad.json()["detail"][0]["loc"])
```

The `loc` path `['body', 'items', 0, 'quantity']` pinpoints the exact field. You wrote no validation code.

## Response models: control what leaves

A `response_model` filters and documents the output. This is how you avoid leaking a field such as a password hash or internal cost.

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class CustomerOut(BaseModel):
    id: int
    name: str

app = FastAPI()

@app.get("/customers/1", response_model=CustomerOut)
def get_customer():
    return {"id": 1, "name": "Ada", "internal_notes": "do not expose"}

print(TestClient(app).get("/customers/1").json())
```

`internal_notes` is gone. Treat the response model as your public contract.

## Raising errors on purpose

For failures that validation cannot see (a missing row), raise `HTTPException`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

STORE = {1: {"id": 1, "name": "Ada"}}
app = FastAPI()

@app.get("/customers/{cid}")
def get_customer(cid: int) -> dict:
    if cid not in STORE:
        raise HTTPException(status_code=404, detail=f"customer {cid} not found")
    return STORE[cid]

client = TestClient(app)
r = client.get("/customers/9")
print(r.status_code, r.json())
```

## Dependency injection

A **dependency** is a function FastAPI calls for you, passing its result into your handler via `Depends`. Use it for anything shared: a database connection, settings, the current user, an API-key check.

```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

def get_prices() -> dict[str, float]:
    return {"P003": 264.62}

app = FastAPI()

@app.get("/price/{sku}")
def price(sku: str, prices: dict = Depends(get_prices)) -> dict:
    return {"sku": sku, "price": prices.get(sku)}

client = TestClient(app)
print(client.get("/price/P003").json())

app.dependency_overrides[get_prices] = lambda: {"P003": 1.0}   # swap in a fake
print(client.get("/price/P003").json())
```

Why bother? Because `dependency_overrides` lets a test replace the real thing (a warehouse connection) with a fake **without touching the handler**. If the handler had called `get_prices()` directly, you could not swap it. This one mechanism is what makes services testable, and you will lean on it for the rest of the stage.

## Common mistakes

- **Calling the dependency yourself.** Writing `prices = get_prices()` inside the handler instead of `Depends(get_prices)` defeats overrides. Symptom: your test's fake is ignored.
- **Mutable default arguments.** `def f(items: list = [])` shares one list across all requests.
- **Forgetting `status_code=201`** on creation routes; FastAPI defaults to 200.
- **Reading a 422 as your bug.** `422 Unprocessable Entity` with a `detail` list means the *caller's* input failed validation; read `loc` and `msg`.
- **Returning a pydantic object and a dict inconsistently.** Pick the response model and return data matching it.

## What to take away

1. A route is a typed function; the hints validate and document it.
2. Path params live in the URL braces; other arguments are query params.
3. Pydantic models validate JSON bodies; failures become `422` with a `loc` and `msg`.
4. `response_model` is the public contract and strips unlisted fields.
5. `Depends` plus `dependency_overrides` is how you make services testable.
6. Test with `TestClient`; never start a server in a test.
