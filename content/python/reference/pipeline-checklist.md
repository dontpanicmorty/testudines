# Pipeline reliability checklist

| Concern | Question to ask | Habit |
|---|---|---|
| Idempotency | Does a rerun give the same result? | delete-then-insert a partition in one transaction, or upsert on a key |
| Logical date | Does the transform read the wall clock? | pass the logical date in as an argument |
| Atomic output | Can a reader see a half-written file? | temp file in the same directory, then `os.replace` |
| Watermark | When is it saved? | after the data is written, never before; never moves backwards |
| Late data | Can rows arrive older than the watermark? | lookback window plus dedupe by key |
| Errors | Transient or permanent? | retry transient with backoff; fail fast on permanent |
| Retries | Is `sleep` injectable? | pass `sleep=` so tests are instant; re-raise after the last attempt |
| Partial failure | Can a rerun resume? | checkpoint plus idempotent steps |
| Bad rows | One bad row, whole job fails? | reject file with reason, plus a reject-rate ceiling |
| Task graph | Order and failure? | topological order; run only if all dependencies succeeded |
| Logs | Can you find one run's lines? | structured JSON with a `run_id`, via `logging` |
| Run table | When did it last succeed? | status, rows in/out, times, watermark per run |
| Quality | Are bad data states caught? | checks return lists of problems; decide block vs warn |
| Freshness and volume | Silent failures? | newest-record age and row count against a baseline |

```python
# no-run
# the incremental job skeleton
state = load_state(path)
rows = plan_incremental(source, state["watermark"], lookback_hours=3)
write_idempotently(rows)
save_state(path, {"watermark": max_updated_at(rows, state["watermark"])})
```

## Alert triage

| Event | Response |
|---|---|
| Retry succeeded | warn in logs |
| Retries exhausted | fail run, alert |
| Few rejected rows | reject file, report count |
| Reject rate above threshold | fail run, alert |
| Stale or empty output | alert |
