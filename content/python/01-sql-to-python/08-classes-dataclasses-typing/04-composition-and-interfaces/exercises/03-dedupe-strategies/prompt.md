Implement a dedupe where *how to pick the survivor* is a swappable **strategy**: a function that takes the list of rows sharing a key (in input order) and returns one row.

- `keep_first(group)` and `keep_last(group)`;
- `keep_max(field)` returns a strategy that picks the row with the greatest `row[field]` (the first such row on ties);
- `dedupe(rows, key, strategy)` returns one row per distinct `row[key]`, ordered by the first appearance of each key. It doesn't modify its input.

```python
rows = [{"id": 1, "v": 3}, {"id": 2, "v": 9}, {"id": 1, "v": 7}]
dedupe(rows, "id", keep_first)        # [{'id': 1, 'v': 3}, {'id': 2, 'v': 9}]
dedupe(rows, "id", keep_last)         # [{'id': 1, 'v': 7}, {'id': 2, 'v': 9}]
dedupe(rows, "id", keep_max("v"))     # [{'id': 1, 'v': 7}, {'id': 2, 'v': 9}]
```
