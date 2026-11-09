A CDC feed delivers rows that can repeat. Write a generator `dedupe(rows, key)` that lazily yields each row the **first** time its key is seen and skips later repeats. `key` is a function from row to a hashable key.

It must work on an endless stream: memory may grow with the number of *distinct* keys, but it must not read ahead.

```python
rows = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
list(dedupe(rows, key=lambda r: r["id"]))
# [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]
```
