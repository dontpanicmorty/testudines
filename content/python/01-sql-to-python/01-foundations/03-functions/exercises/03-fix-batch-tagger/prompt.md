`tag_batch(rows, tags=...)` should return a **new** list of rows where each row (a dict) has a `"tags"` list holding the tags given, plus the automatic tag `"loaded"`.

In production, the second batch of the day carries tags from the first, and sometimes the caller's original rows also change. Fix the function so every call is independent and the input rows are never modified.

```python
tag_batch([{"id": 1}], ["eu"])   # [{"id": 1, "tags": ["eu", "loaded"]}]
tag_batch([{"id": 2}])           # [{"id": 2, "tags": ["loaded"]}]
```
