Write `JsonFormatter`, a `logging.Formatter` subclass whose `format(record)` returns a single-line JSON string with:

- `level` (e.g. `"INFO"`), `logger` (logger name), `message` (the formatted message, so `%s` arguments are applied)
- every key/value from the dict passed as `extra={"fields": {...}}`, merged at the top level
- `exc` containing the formatted traceback text, **only** when the record carries exception info

Output must be valid JSON on one line (no newline characters). Values that are not JSON serialisable (such as a `datetime` or `Path`) must be converted with `str` rather than crashing.

```python
log.info("served %s", "/orders", extra={"fields": {"status": 200, "ms": 12.5}})
# {"level": "INFO", "logger": "access", "message": "served /orders", "status": 200, "ms": 12.5}
```
