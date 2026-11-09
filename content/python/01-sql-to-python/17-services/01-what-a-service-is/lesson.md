+++
id = "services.what-a-service-is"
title = "What a service is"
minutes = 25
+++

# What a service is

Until now your code has been a **script** or a **job**: something starts, does work, exits. dbt run, an Airflow task, a notebook cell: all of those have a beginning and an end, and a scheduler decides when they run.

A **service** is different. It starts once and then *waits*. Other programs send it requests, it answers each one, and it keeps running. It never "finishes".

> **SQL bridge.** A warehouse is a service: you connect, send a query (request), get a result set (response), and the warehouse stays up for the next person. A dbt model is a job: it runs, materialises, ends. This stage teaches you to build the first kind in Python.

## Request in, response out

Every interaction has the same shape:

- A **request**: a *method* (what to do), a *path* (which thing), optional *query parameters*, optional *body*.
- A **response**: a *status code* (how it went) and usually a *body*, most often JSON.

| Method | Meaning | SQL analogue |
|---|---|---|
| `GET` | read, no side effects | `SELECT` |
| `POST` | create something | `INSERT` |
| `PUT` / `PATCH` | replace / modify | `UPDATE` |
| `DELETE` | remove | `DELETE` |

## Status codes you must know

Codes are grouped by the first digit. The group tells the caller *whose fault* a failure is.

| Code | Name | Use it when |
|---|---|---|
| 200 | OK | a read succeeded |
| 201 | Created | a POST made a new thing |
| 204 | No Content | success, nothing to return |
| 400 | Bad Request | the request is malformed |
| 404 | Not Found | that id/path does not exist |
| 409 | Conflict | it would clash with existing state (duplicate) |
| 422 | Unprocessable | well-formed but fails validation |
| 500 | Server Error | *our* bug; the caller did nothing wrong |

The rule: **4xx means the caller should change something; 5xx means they should not bother, we must fix it.**

## JSON is just dicts and lists

A JSON body maps directly onto Python types: object to `dict`, array to `list`, string to `str`, number to `int`/`float`, `null` to `None`.

```python
import json

order = {"order_id": 1001, "status": "shipped", "items": [{"sku": "P003", "qty": 5}]}
wire = json.dumps(order)          # what travels over the network: text
print(wire)
print(json.loads(wire)["items"][0]["qty"])
```

Notice what does **not** survive: tuples become lists, `datetime` and `Decimal` are not JSON at all. You convert them (usually to strings) at the boundary.

## A handler is a function

Strip away the framework and a service is a pile of functions of the form *request data in, (status, body) out*. Modelling handlers as plain functions makes them trivially testable, and that is exactly how frameworks want you to write them.

```python
ORDERS = {1001: {"order_id": 1001, "status": "shipped"}}

def get_order(order_id: int) -> tuple[int, dict]:
    order = ORDERS.get(order_id)
    if order is None:
        return 404, {"error": f"order {order_id} not found"}
    return 200, order

print(get_order(1001))
print(get_order(7))
```

> **Predict first.** What status would `get_order(1001.0)` return? (Hint: dict keys use equality, and `1001 == 1001.0`.)

It returns 200, because `1001.0` hashes and compares equal to `1001`. A real service receives ids as text from the URL, so converting and validating at the edge matters.

## Script vs service: what changes

| Concern | Script / job | Service |
|---|---|---|
| Lifetime | runs then exits | runs until stopped |
| Trigger | schedule or human | someone else's request |
| Failure | job fails, retry later | one bad request must not kill the process |
| State | local variables fine | shared across requests; be careful |
| Output | files, tables | responses, with latency expectations |

Two consequences matter right away:

1. **Errors are data.** In a script you can let an exception crash the run. In a service you convert expected failures into 4xx responses and unexpected ones into a clean 500, and carry on.
2. **State is shared.** The module-level `ORDERS` dict above lives for the whole life of the process and all requests see it. Anything you mutate there is a hidden coupling. We will push state behind dependencies in later lessons.

## Common mistakes

- **Returning 200 with an error message in the body.** Callers and monitoring look at the status code first. Use 404/422/409 honestly.
- **Using 500 for caller mistakes.** If bad input crashes your handler you will see `500 Internal Server Error` for what should be a `422`. Validate first.
- **Using GET to change data.** Browsers, proxies and crawlers retry GETs freely. Writes belong to POST/PUT/DELETE.
- **Returning a raw exception message.** `KeyError: 'email'` leaks internals and means nothing to the caller. Return a clear, stable error body.

## What to take away

1. A service starts once, waits for requests, and answers each one; a job runs and exits.
2. A request is method + path (+ query + body); a response is status + body.
3. 2xx success, 4xx the caller must change something, 5xx we must fix it.
4. JSON bodies are dicts and lists; convert dates and decimals at the boundary.
5. Think of a handler as `data in -> (status, body) out`, and keep it a testable function.
