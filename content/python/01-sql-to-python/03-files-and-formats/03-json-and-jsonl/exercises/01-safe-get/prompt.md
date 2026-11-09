Write `dig(obj, *keys, default=None)` that walks nested dicts and lists following `keys` and returns the value found, or `default` if any step is missing (missing key, index out of range, or the current value is `None`/not subscriptable).

```python
doc = {"user": {"tags": ["a", "b"]}, "props": None}
dig(doc, "user", "tags", 1)            # "b"
dig(doc, "props", "path")              # None
dig(doc, "user", "plan", default="free")   # "free"
```
