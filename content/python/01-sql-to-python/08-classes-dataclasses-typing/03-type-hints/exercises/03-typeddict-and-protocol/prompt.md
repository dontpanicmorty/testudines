Complete `solution.py` so it passes `mypy --strict` and behaves as described.

- `Event` is a `TypedDict` with `user_id: int`, `name: str`, `value: float`.
- `Sink` is already a `Protocol` with `write(events) -> int`.
- `ListSink` collects events in an attribute `events` (a list); `write` appends them and returns how many were stored. It must **not** inherit from `Sink`.
- `route(events, sink, *, min_value=0.0)` sends the events whose `value >= min_value` to `sink.write` in a **single call** (keeping order) and returns what `write` returns. If no event qualifies, it doesn't call `write` and returns `0`.

```python
sink = ListSink()
route([{"user_id": 1, "name": "click", "value": 2.5}], sink, min_value=1.0)   # 1
```

A checker file also verifies that wrong value types in an `Event` are rejected by mypy, so give each field its precise type. No `Any`, `cast` or `# type: ignore` in `solution.py`.
