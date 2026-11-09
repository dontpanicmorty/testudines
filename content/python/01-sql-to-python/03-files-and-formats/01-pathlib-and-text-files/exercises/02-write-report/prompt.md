Write `write_daily_report(out_dir, day, lines)`.

- Create `out_dir` (and parents) if missing.
- Write `<out_dir>/<day>.txt` containing each line followed by `"\n"`, UTF-8.
- Calling it twice for the same day **replaces** the file (idempotent: no duplicated lines).
- Return the `Path` of the file.

```python
p = write_daily_report(Path("out/reports"), "2025-06-01", ["ok: 10", "failed: 2"])
p.read_text(encoding="utf-8")   # "ok: 10\nfailed: 2\n"
```
