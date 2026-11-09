+++
id = "pipelines.retries-checkpoints-and-failure"
title = "Retries, checkpoints and failure"
minutes = 30
+++

# Retries, checkpoints and failure

Pipelines talk to networks, warehouses and files other people write. Things fail. The question is not whether, but what your code does next.

> **Snowflake/dbt bridge.** You have seen `dbt build` stop at a failed model and skip everything downstream, and `dbt retry` resume from the failure. You have seen a warehouse timeout that works on the second try, and a SQL compilation error that never will. The skill is telling those two apart.

## Transient versus permanent errors

- **Transient**: it may succeed if you try again. Connection reset, timeout, HTTP 429 or 5xx, a lock held by another job.
- **Permanent**: retrying is pointless. Bad credentials, HTTP 400/404, a `ValueError` parsing a malformed row, a SQL syntax error.

Retrying a permanent error wastes time and can hammer a service. Not retrying a transient one pages a human for nothing.

```python
class HttpError(Exception):
    def __init__(self, status):
        super().__init__(f"HTTP {status}")
        self.status = status

def is_transient(exc: Exception) -> bool:
    if isinstance(exc, (ConnectionError, TimeoutError)):
        return True
    if isinstance(exc, HttpError):
        return exc.status == 429 or exc.status >= 500
    return False

for e in [TimeoutError(), HttpError(503), HttpError(404), ValueError("bad")]:
    print(type(e).__name__, is_transient(e))
```

## A retry policy

A policy has three parts: **how many** attempts, **how long** to wait, and **which** errors qualify. Wait with *exponential backoff* (1s, 2s, 4s...) so a struggling service gets room to recover, and add jitter in real systems so many clients don't retry in lockstep.

```python
import time

def retry(fn, attempts, is_retryable, base_delay=1.0, sleep=time.sleep):
    for n in range(attempts):
        try:
            return fn()
        except Exception as exc:
            if not is_retryable(exc) or n == attempts - 1:
                raise
            sleep(base_delay * 2 ** n)

calls = {"n": 0}
waits = []

def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise TimeoutError("slow")
    return "ok"

print(retry(flaky, 5, lambda e: isinstance(e, TimeoutError), sleep=waits.append))
print(calls, waits)
```

Notice `sleep` is a parameter. That is a **seam**: tests (and this lesson) pass `waits.append` and run instantly. Code that calls `time.sleep` directly is slow to test and tends to be tested badly.

In real projects you may reach for the `tenacity` library, which packages exactly these ideas as a decorator. Understand the loop first; the library then reads as configuration.

Always **re-raise** after the last attempt. Swallowing the final error turns a failure into silent success.

## Partial failure and checkpoints

A job that processes 500 files and dies on file 412 should not redo 411 files. A **checkpoint** records progress durably so a rerun resumes.

```python
import json, tempfile
from pathlib import Path

def process_all(items, handle, checkpoint: Path):
    done = set(json.loads(checkpoint.read_text())) if checkpoint.exists() else set()
    for item in items:
        if item in done:
            continue
        handle(item)
        done.add(item)
        checkpoint.write_text(json.dumps(sorted(done)))

with tempfile.TemporaryDirectory() as d:
    cp = Path(d) / "cp.json"
    seen = []
    def handle(x):
        if x == "c" and not seen.count("retry"):
            seen.append("retry")
            raise RuntimeError("boom")
        seen.append(x)
    try:
        process_all(["a", "b", "c", "d"], handle, cp)
    except RuntimeError:
        print("failed, checkpoint:", cp.read_text())
    process_all(["a", "b", "c", "d"], handle, cp)
    print(seen)
```

The rerun skips `a` and `b`. This only works because each item is handled idempotently: if the crash happens after `handle` but before the checkpoint write, that item runs again.

## Reject files: don't fail the whole load for one bad row

Some failures belong to a *row*, not the *job*. Parse what you can, set aside what you cannot, and keep the evidence. A **dead-letter** (reject) file stores the bad record with the reason so someone can fix and replay it.

```python
import json

def parse_row(raw):
    return {"id": int(raw["id"]), "amount": float(raw["amount"])}

good, rejects = [], []
for raw in [{"id": "1", "amount": "9.5"}, {"id": "x", "amount": "2"}, {"id": "3", "amount": ""}]:
    try:
        good.append(parse_row(raw))
    except ValueError as exc:
        rejects.append({"row": raw, "error": str(exc)})

print(good)
print(json.dumps(rejects, indent=1))
```

Set a ceiling. Rejecting 3 of 1,000,000 rows is normal; rejecting 40% means the schema changed and the job should fail loudly.

## Alert-worthy or ignorable?

| Situation | Action |
|---|---|
| Retry succeeded on attempt 2 | log a warning, no page |
| Retries exhausted | fail the run, alert |
| A handful of rejected rows | write reject file, report the count |
| Reject rate above threshold | fail, alert |
| Same task failing every night | alert about the *pattern*, not each instance |

An alert should mean "a human must act". If people learn to ignore alerts, the real one gets ignored too.

## Common mistakes

- `except Exception: pass` around the whole job. The error disappears and the run reports success.
- Bare `except:` also catches `KeyboardInterrupt`.
- Retrying non-idempotent work (a non-upsert insert) and duplicating rows.
- Backoff that is too small, or no maximum, turning a brief outage into a retry storm.

## What to take away

1. Classify errors: retry transient ones, fail fast on permanent ones.
2. Backoff grows exponentially; inject `sleep` so it is testable; re-raise after the last attempt.
3. Checkpoints plus idempotent steps make reruns cheap and safe.
4. Bad rows go to a reject file with the reason, up to a threshold.
5. Alert on actionable failures, not on every blip.
