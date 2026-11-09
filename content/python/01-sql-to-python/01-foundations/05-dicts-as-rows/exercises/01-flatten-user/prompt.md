Events look like `{"user": {"id": 7, "geo": {"country": "DE"}}, "props": {"plan": "pro"}}`, but any level may be missing.

Write `flatten_event(event)` returning `{"user_id": ..., "country": ..., "plan": ...}`. Missing values are `None`, except `plan`, which defaults to `"free"`.

```python
flatten_event({"user": {"id": 7, "geo": {"country": "DE"}}, "props": {"plan": "pro"}})
# {"user_id": 7, "country": "DE", "plan": "pro"}
flatten_event({"user": {"id": 8}})
# {"user_id": 8, "country": None, "plan": "free"}
flatten_event({})
# {"user_id": None, "country": None, "plan": "free"}
```
