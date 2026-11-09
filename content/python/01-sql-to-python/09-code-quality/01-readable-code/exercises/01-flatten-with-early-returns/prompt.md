`classify_order` works but is nested four levels deep, and a recent change to it was misread in code review. Refactor it with early returns **without changing its behaviour**:

- `None` order: `"missing"`
- status other than `"complete"`: `"open"`
- total missing or `<= 0`: `"empty"`
- country `"US"`: `"domestic"`; otherwise `"international"`

```python
classify_order({"status": "complete", "total": 50, "country": "US"})   # "domestic"
classify_order(None)                                                  # "missing"
```

The check also measures nesting depth: no more than two nested control-flow levels (an `elif` chain counts as one level).
