+++
id = "pipelines.incremental-loads"
title = "Incremental loads and watermarks"
minutes = 30
+++

# Incremental loads and watermarks

Reloading ten years of orders every night is wasteful. An **incremental load** reads only what changed since last time. The hard part is "since last time": you need to remember where you stopped.

> **dbt bridge.** In an incremental model you write `where updated_at > (select max(updated_at) from {{ this }})`. The target table itself is the state. In plain Python you often don't have a convenient target to query, so you keep the state explicitly: a **watermark** saved in a file or a metadata table.

## The watermark pattern

The watermark is the highest value of a monotonically increasing column (usually `updated_at`) you have fully processed.

```python
source = [
    {"id": 1, "updated_at": "2026-01-01T09:00:00"},
    {"id": 2, "updated_at": "2026-01-01T10:30:00"},
    {"id": 3, "updated_at": "2026-01-02T08:15:00"},
]

def extract_since(rows, watermark):
    new = [r for r in rows if watermark is None or r["updated_at"] > watermark]
    new.sort(key=lambda r: r["updated_at"])
    next_mark = max((r["updated_at"] for r in new), default=watermark)
    return new, next_mark

batch, mark = extract_since(source, None)       # first run: everything
print(len(batch), mark)
batch, mark = extract_since(source, mark)       # second run: nothing new
print(len(batch), mark)
```

ISO-8601 timestamps sort correctly as plain strings, which is why they are the right interchange format. Note `default=watermark`: when nothing is new, the watermark must **not** move backwards or become `None`.

## Where to keep the state

A small JSON file works for a single job. Save it **after** the data is safely written, and write it atomically (lesson 1).

```python
import json, os, tempfile
from pathlib import Path

def load_state(path):
    p = Path(path)
    if not p.exists():
        return {"watermark": None}
    return json.loads(p.read_text())

def save_state(path, state):
    p = Path(path)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, sort_keys=True))
    os.replace(tmp, p)

with tempfile.TemporaryDirectory() as d:
    sp = Path(d) / "orders.state.json"
    print(load_state(sp))
    save_state(sp, {"watermark": "2026-01-02T08:15:00"})
    print(load_state(sp))
```

The order of operations is the whole game:

1. read watermark
2. extract rows newer than it
3. write rows (idempotently)
4. **only then** save the new watermark

If the job dies after step 3 but before step 4, the next run re-reads the same rows. Because step 3 is idempotent (an upsert), that is harmless. This is called **at-least-once delivery plus idempotent writes**, and it is the practical way to get correct results.

## Late-arriving data

> **Predict first.** A row with `updated_at = 10:00` is committed to the source at 11:05, after your 11:00 run set the watermark to 10:45. Does the next run pick it up?

No. `10:00 > 10:45` is false, so the row is skipped forever. Sources commit out of order: long transactions, replication lag, upstream batch jobs that backdate events.

The standard cure is a **lookback window**: re-read a margin before the watermark and let the idempotent upsert absorb the overlap.

```python
from datetime import datetime, timedelta

def window_start(watermark, lookback_hours):
    if watermark is None:
        return None
    start = datetime.fromisoformat(watermark) - timedelta(hours=lookback_hours)
    return start.isoformat()

print(window_start("2026-01-02T08:15:00", 3))
print(window_start(None, 3))
```

This is what dbt's `lookback` patterns and "reprocess the last 3 days" incremental strategies do. It trades extra reads for correctness. Pick the window from how late your source can really be, not from a guess.

## Deduplicating the overlap

With a lookback you will see some rows twice, and the same id may appear in several versions. Keep the latest version per key:

```python
rows = [
    {"id": 1, "v": "a", "updated_at": "2026-01-01T09:00:00"},
    {"id": 1, "v": "b", "updated_at": "2026-01-01T11:00:00"},
    {"id": 2, "v": "c", "updated_at": "2026-01-01T10:00:00"},
]
latest = {}
for r in sorted(rows, key=lambda r: r["updated_at"]):
    latest[r["id"]] = r
print(list(latest.values()))
```

Sorting first and letting later rows overwrite earlier ones is the Python spelling of `row_number() over (partition by id order by updated_at desc) = 1`.

## Backfills

A backfill is an incremental job with the watermark forced somewhere else. Design for it from day one: accept an explicit `start` and `end` instead of only reading state, and make sure running a backfill does not move the production watermark backwards. A common rule: `new_watermark = max(old_watermark, max_seen)`.

Some changes cannot be handled incrementally at all: a business rule changes, or deletes in the source. Those need a **full refresh**, the equivalent of `dbt run --full-refresh`. Hard deletes are invisible to a watermark; use a soft-delete flag, a periodic full compare, or a change log.

## Common mistakes

- Saving the watermark before the write succeeds: a crash loses data silently.
- Using `>=` on a timestamp with duplicates at the boundary without an idempotent write: infinite duplicates. Using `>` without a lookback: missed rows. You need one of: idempotent write plus `>=`, or lookback.
- Computing the watermark from `datetime.now()` instead of from the data you saw.
- `TypeError: '>' not supported between instances of 'NoneType' and 'str'` from comparing against a missing first-run watermark.

## What to take away

1. A watermark is explicit state: the highest value you have fully processed.
2. Write data first, move the watermark second.
3. At-least-once reads plus idempotent writes give correct results.
4. Late data needs a lookback window; dedupe the overlap by key.
5. Backfills and full refreshes must be possible without corrupting the watermark.
