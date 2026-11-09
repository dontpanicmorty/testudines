Write `evaluate_run(metrics, max_age_hours=24, low=0.5, high=2.0, max_reject_rate=0.05)` returning a list of alert codes for a finished run.

`metrics` is a dict with keys `rows_written`, `previous_rows` (may be `None`), `rows_rejected`, `latest_record` (ISO timestamp of the newest row, or `None`) and `now` (ISO timestamp).

Alerts, in this order:

1. `"stale"`: `latest_record` is `None`, or older than `max_age_hours` (strictly greater).
2. `"volume_drop"`: `rows_written / previous_rows < low`; or `"volume_spike"`: ratio `> high`. Skipped when `previous_rows` is `None` or `0`.
3. `"rejects"`: `rows_rejected / (rows_written + rows_rejected) > max_reject_rate`. Skipped when both are zero.

```python
evaluate_run({"rows_written": 100, "previous_rows": 500, "rows_rejected": 0,
              "latest_record": "2026-01-02T08:00:00", "now": "2026-01-02T09:00:00"})
# ["volume_drop"]
```
