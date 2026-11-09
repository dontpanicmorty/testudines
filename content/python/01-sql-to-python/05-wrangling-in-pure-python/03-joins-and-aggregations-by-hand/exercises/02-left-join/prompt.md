Write `left_join(left, right, on, right_columns)`.

- `left`, `right` are lists of dicts; `on` is the key present in both.
- For each left row (original order) output one dict per matching right row: the left columns plus the listed `right_columns` taken from that right row.
- A left row with no match is kept once, with every right column set to `None`.
- Matches keep their order from `right`. Inputs must not be modified.

```python
left_join([{"id": 1}, {"id": 2}], [{"id": 1, "x": "a"}, {"id": 1, "x": "b"}], "id", ["x"])
# [{"id": 1, "x": "a"}, {"id": 1, "x": "b"}, {"id": 2, "x": None}]
```
