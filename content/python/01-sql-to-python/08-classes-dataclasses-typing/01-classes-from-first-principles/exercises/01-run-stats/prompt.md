Implement `RunStats`, a small counter a loader uses to report how a run went.

- `RunStats()` starts with `rows_read == 0` and `rows_rejected == 0`.
- `record(ok)` counts one row read, and one rejected when `ok` is false.
- `reject_rate` (a property) is `rows_rejected / rows_read`, or `0.0` when nothing was read.
- `repr(stats)` looks like `RunStats(read=3, rejected=1)`.

```python
s = RunStats()
for ok in [True, False, True]:
    s.record(ok)
print(s)             # RunStats(read=3, rejected=1)
print(s.reject_rate) # 0.3333333333333333
```
