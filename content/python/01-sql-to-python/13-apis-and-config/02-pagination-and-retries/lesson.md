+++
id = "apis-and-config.pagination-and-retries"
title = "Pagination, retries and rate limits"
minutes = 30
+++

# Pagination, retries and rate limits

APIs hand you data in pages and fail in ordinary, temporary ways. Your job is to turn that into one clean stream of records and to retry only what is safe to retry.

> **Snowflake bridge.** Pagination is `LIMIT/OFFSET` (or keyset `WHERE id > :last`) done over HTTP. Retries are what the warehouse does when a transient `Warehouse is resuming` hits your query. The difference: *you* have to write that loop.

## Pagination as a generator

Two common styles: **page numbers** (`?page=2`) and **cursors** (`?cursor=abc`, the server tells you where to resume). The loop is the same: fetch, yield each record, stop when there is no next pointer. A generator yields lazily, so a caller who needs 5 records never triggers 50 requests.

```python
import httpx
from collections.abc import Iterator

PAGES = {
    None: {"data": [1, 2, 3], "next_cursor": "a"},
    "a": {"data": [4, 5], "next_cursor": "b"},
    "b": {"data": [6], "next_cursor": None},
}
requests_made = []

def handler(request):
    cursor = request.url.params.get("cursor")
    requests_made.append(cursor)
    return httpx.Response(200, json=PAGES[cursor])

def iter_records(client: httpx.Client) -> Iterator[int]:
    cursor = None
    while True:
        params = {"cursor": cursor} if cursor else {}
        resp = client.get("/items", params=params)
        resp.raise_for_status()
        body = resp.json()
        yield from body["data"]
        cursor = body["next_cursor"]
        if cursor is None:
            return

client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")
print(list(iter_records(client)))
print(requests_made)
```

> **Predict first.** If you take only the first two records with `itertools.islice(iter_records(client), 2)`, how many requests are made?

```python
import httpx
from itertools import islice

calls = []
def handler(request):
    calls.append(request.url.params.get("page"))
    return httpx.Response(200, json={"data": [1, 2, 3], "next_cursor": "x"})

client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")

def iter_records(client):
    cursor = None
    while True:
        body = client.get("/items", params={"page": cursor or "first"}).json()
        yield from body["data"]
        cursor = body["next_cursor"]

print(list(islice(iter_records(client), 2)), len(calls))
```

One. The generator pauses at the second `yield` and never fetches page 2.

## Which failures deserve a retry?

| Signal | Meaning | Retry? |
|---|---|---|
| timeout, connection reset | transient network | yes |
| 500, 502, 503, 504 | server trouble | yes, with backoff |
| 429 | you are going too fast | yes, after the wait they ask for (`Retry-After`) |
| 400, 401, 403, 404, 422 | your request is wrong | **no**, retrying repeats the mistake |

## Exponential backoff with jitter, by hand

Wait longer after each failure: `base * 2**attempt`, capped. Add **jitter** (randomness) so 200 workers that failed together don't all retry in the same instant. "Full jitter" picks a random wait between 0 and the capped ceiling. Inject both `sleep` and the random generator so tests are instant and deterministic.

```python
import random

def delays(retries: int, base: float = 0.5, cap: float = 8.0, rng: random.Random | None = None) -> list[float]:
    out = []
    for attempt in range(retries):
        ceiling = min(cap, base * 2 ** attempt)
        out.append(rng.uniform(0, ceiling) if rng else ceiling)
    return out

print(delays(6))
print([round(d, 3) for d in delays(6, rng=random.Random(42))])
```

```python
import time

def call_with_retry(fn, retries=3, sleep=time.sleep):
    for attempt in range(retries + 1):
        try:
            return fn()
        except ConnectionError:
            if attempt == retries:
                raise
            sleep(0.5 * 2 ** attempt)

state = {"n": 0}
def flaky():
    state["n"] += 1
    if state["n"] < 3:
        raise ConnectionError("reset by peer")
    return "ok"

slept = []
print(call_with_retry(flaky, sleep=slept.append), state["n"], slept)
```

## A fake flaky server

Script the failures, then assert the client copes. This is how you test retry code without waiting or hoping.

```python
import httpx

def scripted(statuses):
    it = iter(statuses)
    def handler(request):
        status = next(it)
        headers = {"Retry-After": "2"} if status == 429 else {}
        return httpx.Response(status, json={"ok": status == 200}, headers=headers)
    return httpx.MockTransport(handler)

client = httpx.Client(transport=scripted([503, 429, 200]), base_url="https://api.example.test")
for _ in range(3):
    r = client.get("/x")
    print(r.status_code, r.headers.get("retry-after"))
```

## 429 and Retry-After

A rate-limited server often says how long to wait. Prefer that over your own guess: `Retry-After: 2` means sleep two seconds. Better still, avoid being limited: pace your calls and keep concurrency small.

## tenacity, the library version

Once you understand the loop, let `tenacity` own it. It is declarative: *when* to retry, *how long* to wait, *when to give up*.

```python
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_none

calls = {"n": 0}

@retry(
    retry=retry_if_exception_type(ConnectionError),
    stop=stop_after_attempt(4),
    wait=wait_none(),          # in production: wait_exponential(multiplier=0.5, max=8) + wait_random(0, 1)
    reraise=True,              # raise the real error, not tenacity.RetryError
)
def fetch():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("blip")
    return "payload"

print(fetch(), calls["n"])
```

Always set `reraise=True` unless you want to handle `tenacity.RetryError`, and always limit attempts.

## Idempotency: retries must be safe

A `GET` is naturally repeatable. A `POST /payments` that times out may or may not have been applied. Retrying could charge twice. The fix is an **idempotency key**: a unique id you generate once per logical operation and send with every attempt; the server remembers it and replays the first result.

```python
import httpx

seen = {}
def handler(request):
    key = request.headers["Idempotency-Key"]
    if key in seen:
        return httpx.Response(200, json={**seen[key], "replayed": True})
    seen[key] = {"order_id": len(seen) + 1}
    return httpx.Response(201, json=seen[key])

client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")
h = {"Idempotency-Key": "load-2026-11-02-batch-7"}
print(client.post("/orders", headers=h).json())
print(client.post("/orders", headers=h).json())
```

This is the same idea as a `MERGE` keyed on a business key: running it twice leaves the same end state.

## Common mistakes

- Retrying every error, including `401` and `422`: you hammer a server with a request that can never succeed.
- Retry loops without a cap on attempts or wait time. `while True` plus a dead server is an outage you caused.
- No jitter, so every worker retries at once.
- `time.sleep` baked into the function: tests take minutes. Inject `sleep`.
- tenacity without `reraise=True` raising `tenacity.RetryError: RetryError[<Future at 0x... state=finished raised ConnectionError>]` and hiding the real cause.
- Retrying non-idempotent writes with no idempotency key.

## What to take away

1. Wrap pagination in a generator; yielding lazily keeps memory and request count low.
2. Retry timeouts, 5xx and 429. Do not retry other 4xx.
3. Back off exponentially, cap it, add jitter, honour `Retry-After`.
4. Inject `sleep` and randomness so retry logic is instant and deterministic in tests.
5. tenacity declares the policy; always bound attempts and use `reraise=True`.
6. Writes need idempotency keys (or a natural idempotent design) before they can be retried.
