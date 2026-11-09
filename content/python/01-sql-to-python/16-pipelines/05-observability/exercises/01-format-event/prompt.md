Write `format_event(event, **fields)` returning a **single-line JSON string** with an `"event"` key plus all the extra fields, keys sorted alphabetically.

Also write `parse_events(text)` that takes multi-line log text and returns the list of dicts for lines that are valid JSON objects, ignoring blank lines and non-JSON lines.

```python
format_event("load_finished", table="orders", rows=500)
# '{"event": "load_finished", "rows": 500, "table": "orders"}'
parse_events('{"event": "a"}\nnot json\n\n{"event": "b"}')   # [{"event": "a"}, {"event": "b"}]
```
