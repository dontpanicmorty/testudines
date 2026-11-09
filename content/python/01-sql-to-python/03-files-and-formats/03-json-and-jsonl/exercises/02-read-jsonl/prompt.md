Write `read_events(path)` returning `(events, bad_count)`.

- `events` is the list of dicts parsed from valid lines, in order.
- Blank lines are ignored and are **not** counted as bad.
- A line that is not valid JSON counts as bad. A line that is valid JSON but not an object (like `42` or `[1]`) is also bad.

```python
# {"id": 1}\n{"id": 2\n\n[1]\n{"id": 3}
read_events(path)   # ([{"id": 1}, {"id": 3}], 2)
```
