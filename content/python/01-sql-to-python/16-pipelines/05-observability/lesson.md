+++
id = "pipelines.observability"
title = "Observability for pipelines"
minutes = 30
+++

# Observability for pipelines

A pipeline that runs without raising an error can still be wrong: yesterday's data never arrived, a join dropped half the rows, a column went null. Observability is how you find out before your stakeholders do.

> **dbt bridge.** `dbt test` (`not_null`, `unique`, `accepted_values`), source freshness, and the `run_results.json` artifact are three observability tools. This lesson builds the same three in plain Python: assertions on data, freshness checks, and a record of every run.

## Structured logs

`print("loaded 500 rows")` is readable to you and useless to a machine. A **structured log** is one JSON object per line with consistent field names, so you can filter, count and chart it later.

```python
import json
import logging
import sys

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {"level": record.levelname, "event": record.getMessage()}
        payload.update(getattr(record, "fields", {}))
        return json.dumps(payload, sort_keys=True)

log = logging.getLogger("pipeline")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
log.addHandler(handler)
log.setLevel(logging.INFO)

log.info("load_finished", extra={"fields": {"table": "orders", "rows": 500, "run_id": "abc123"}})
log.warning("late_rows", extra={"fields": {"table": "orders", "count": 12}})
```

Use `logging`, not `print`, in pipeline code: levels, handlers and formatting come free. Always include a `run_id` so every line from one run can be pulled together. Never log secrets or whole rows of personal data.

## A run metadata table

Logs scroll away. Keep a durable record of each run: a table you can query for "when did orders last succeed and how many rows did it write?". This is a table you'd build in the warehouse; sqlite stands in here.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""
    create table pipeline_runs (
        run_id text primary key, pipeline text, logical_date text,
        status text, rows_written int, started_at text, finished_at text
    )
""")

def record_run(conn, run_id, pipeline, logical_date, status, rows, started, finished):
    with conn:
        conn.execute(
            "insert or replace into pipeline_runs values (?,?,?,?,?,?,?)",
            (run_id, pipeline, logical_date, status, rows, started, finished),
        )

record_run(conn, "r1", "orders", "2026-01-01", "success", 500, "2026-01-02T01:00:00", "2026-01-02T01:03:10")
record_run(conn, "r2", "orders", "2026-01-02", "failed", 0, "2026-01-03T01:00:00", "2026-01-03T01:00:20")
print(conn.execute("select pipeline, max(logical_date) from pipeline_runs where status='success' group by 1").fetchall())
```

## Data quality assertions as code

A quality check is a function from data to a list of problems. Returning problems (instead of raising on the first one) lets you report everything wrong at once.

```python
def check_orders(rows):
    problems = []
    if not rows:
        problems.append("no rows")
    ids = [r["order_id"] for r in rows]
    if any(i is None for i in ids):
        problems.append("null order_id")
    non_null = [i for i in ids if i is not None]
    if len(non_null) != len(set(non_null)):
        problems.append("duplicate order_id")
    if any(r["amount"] < 0 for r in rows):
        problems.append("negative amount")
    return problems

print(check_orders([{"order_id": 1, "amount": 5}, {"order_id": 1, "amount": -2}]))
print(check_orders([{"order_id": 1, "amount": 5}]))
```

These are `not_null`, `unique` and a custom expression test. Decide per check whether failure should **block** the run (corrupt keys) or only **warn** (a small volume dip).

## Row counts and freshness

Two cheap checks catch most silent failures.

**Freshness**: how old is the newest record? **Volume**: is today's count wildly different from yesterday's?

```python
from datetime import datetime

def age_hours(latest_iso, now_iso):
    delta = datetime.fromisoformat(now_iso) - datetime.fromisoformat(latest_iso)
    return delta.total_seconds() / 3600

print(age_hours("2026-01-01T06:00:00", "2026-01-02T09:30:00"))

def volume_ratio(today, previous):
    return None if not previous else today / previous

print(volume_ratio(480, 500), volume_ratio(100, 500), volume_ratio(10, 0))
```

Compare against expectations that fit the data: a weekend dip may be normal. A fixed ratio band is a start; a rolling average per weekday is better.

## Metrics a pipeline should emit

At the end of every run, emit a few numbers:

- rows read, rows written, rows rejected
- duration in seconds
- watermark before and after
- age of the newest record (freshness)
- number of retries used

Row-in vs row-out is the most valuable: a join that quietly multiplies or drops rows shows up immediately. Store these in the run table next to the status.

## Common mistakes

- Logging the exception message but not the `run_id`, then being unable to find the other lines.
- Quality checks that raise `KeyError` on a missing column instead of reporting "missing column" as a problem.
- Alerting on everything, so the channel is muted.
- Checking only that the job succeeded, not that it wrote anything: an empty success is still a failure.

## What to take away

1. Emit structured logs with a `run_id`, using `logging`.
2. Record every run (status, counts, times) in a queryable table.
3. Express data quality as functions that return lists of problems.
4. Freshness and volume checks catch most silent failures.
5. Emit rows in/out, duration and watermarks every run.
