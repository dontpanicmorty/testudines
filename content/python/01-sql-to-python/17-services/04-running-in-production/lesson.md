+++
id = "services.running-in-production"
title = "Running in production"
minutes = 30
+++

# Running in production

A service that passes its tests is not yet a service you can run. Production adds questions a notebook never asks: what process actually listens on the port, how do you stop it without dropping requests, how do you find the one failing request in a million, and what happens when a downstream call hangs?

> **SQL bridge.** You have debugged slow queries with `QUERY_HISTORY`: who ran what, how long, with what result. Structured request logging is the same idea for your own service, and a request id is the query id you grep for.

## Who runs your app: uvicorn and workers

FastAPI is an *application*; it needs a *server* to speak HTTP. That server is **uvicorn**. You hand it the import path of your app:

```bash
# no-run
uvicorn mypkg.api:app --host 0.0.0.0 --port 8000 --workers 4
```

A **worker** is a separate OS process running its own copy of the app. Four workers handle four requests truly in parallel (Python's GIL limits threads within one process, not across processes). Consequences you must design for:

- **Workers share nothing.** A module-level dict is *per worker*. Anything that must be consistent (idempotency keys, caches that matter, counters) lives in a database or shared store, not in memory.
- **Startup cost is multiplied.** Loading a 2 GB model in each of four workers costs 8 GB.
- A sensible starting point is a worker count near the number of CPU cores for CPU-bound handlers, and fewer for I/O-bound async ones. Measure; do not guess.

## Startup and graceful shutdown with lifespan

Create expensive resources (connection pools, HTTP clients) **once at startup**, and release them at shutdown. FastAPI's `lifespan` is a context manager wrapping the app's whole life. On a stop signal, uvicorn stops accepting new connections, lets in-flight requests finish, then runs your cleanup: that is a *graceful shutdown*.

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

events = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    events.append("startup")
    app.state.pool = {"connected": True}      # stand-in for a real pool
    yield
    app.state.pool["connected"] = False
    events.append("shutdown")

app = FastAPI(lifespan=lifespan)

@app.get("/ping")
def ping(request: Request) -> dict:
    return {"pool": request.app.state.pool["connected"]}

with TestClient(app) as client:        # the with-block runs startup and shutdown
    print(client.get("/ping").json())
print(events)
```

Without the `with`, `TestClient` does not run lifespan; that is a classic source of "works in prod, `AttributeError` in tests".

## Structured logging, one line per request

`print` is not logging. In production you want each log record to be a machine-parseable line (JSON) with consistent fields, so a log system can filter `status >= 500` or follow one `request_id`.

```python
import json
import logging

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {"level": record.levelname, "logger": record.name, "message": record.getMessage()}
        payload.update(getattr(record, "fields", {}))
        return json.dumps(payload, sort_keys=True)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
log = logging.getLogger("access")
log.addHandler(handler)
log.setLevel(logging.INFO)
log.propagate = False

log.info("request", extra={"fields": {"method": "GET", "path": "/orders", "status": 200}})
```

The `extra=` argument attaches fields to the record. Never log secrets, tokens or full request bodies.

## Middleware: code around every request

A **middleware** wraps each request: it can read the request, call the real handler, then adjust the response. It is the right place for cross-cutting concerns: request ids, timing, access logs.

```python
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    request.state.request_id = request_id
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Elapsed-Ms"] = f"{(time.perf_counter() - started) * 1000:.1f}"
    return response

@app.get("/ping")
def ping(request: Request) -> dict:
    return {"request_id": request.state.request_id}

client = TestClient(app)
r = client.get("/ping", headers={"X-Request-ID": "abc123"})
print(r.headers["x-request-id"], r.json())
print(len(client.get("/ping").headers["x-request-id"]))
```

If the caller sends an id, reuse it so one id follows a request across services; otherwise mint one.

## Timeouts: never wait forever

Every call to something you do not control (another service, a warehouse) needs a timeout. Without one, a hung dependency ties up your workers until the service stops answering. In async code `asyncio.wait_for` enforces it; answer with `504 Gateway Timeout` rather than hanging.

```python
import asyncio

async def slow_lookup() -> str:
    await asyncio.sleep(0.2)
    return "done"

async def main() -> None:
    try:
        print(await asyncio.wait_for(slow_lookup(), timeout=0.05))
    except asyncio.TimeoutError:
        print("gave up after 50 ms")

asyncio.run(main())
```

## Containers, conceptually

A container image is a frozen filesystem holding your code, a Python interpreter and your dependencies, so "it runs on my machine" becomes "it runs in the image". The habits that matter:

```dockerfile
# no-run
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY src ./src
USER nobody
EXPOSE 8000
CMD ["uvicorn", "mypkg.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

- **Configuration comes from environment variables**, never baked into the image.
- **Log to stdout/stderr.** The platform collects them; do not write log files inside the container.
- **Run as a non-root user** and keep the image small.
- Expose a **health endpoint** the platform can probe, and handle `SIGTERM` (uvicorn does) so deploys do not drop requests.

## Common mistakes

- **Per-worker state treated as global.** The counter is right in tests (one process) and wrong with four workers.
- **`TestClient(app)` without `with` when you rely on lifespan.** Startup never runs.
- **No timeout on outbound calls.** One slow dependency freezes everything.
- **Logging with f-strings of whole payloads.** Leaks personal data and cannot be queried; log fields instead.
- **Catching `Exception` in middleware and returning nothing.** Errors vanish; log with the request id, then re-raise or return a 500.

## What to take away

1. uvicorn serves the app; workers are separate processes that share nothing.
2. Use `lifespan` for startup/shutdown; graceful shutdown lets in-flight requests finish.
3. Log one structured (JSON) line per request with a request id.
4. Middleware is the home for request ids, timing and access logs.
5. Put a timeout on every outbound call and map it to `504`.
6. Containers: config from env, logs to stdout, non-root, health endpoint.
