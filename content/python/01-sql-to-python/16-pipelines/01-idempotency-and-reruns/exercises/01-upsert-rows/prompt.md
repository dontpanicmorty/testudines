A customer sync receives batches that may repeat rows or carry newer versions of rows already loaded.

Write `upsert(existing, incoming, key)` that returns a **new list**: rows from `incoming` replace rows in `existing` with the same `key` value, and unseen keys are added at the end. Existing order is preserved and the input lists must not be modified.

```python
existing = [{"id": 1, "plan": "free"}, {"id": 2, "plan": "pro"}]
incoming = [{"id": 2, "plan": "team"}, {"id": 3, "plan": "free"}]
upsert(existing, incoming, "id")
# [{"id": 1, "plan": "free"}, {"id": 2, "plan": "team"}, {"id": 3, "plan": "free"}]
```

Applying the same `incoming` twice must give the same result as applying it once.
