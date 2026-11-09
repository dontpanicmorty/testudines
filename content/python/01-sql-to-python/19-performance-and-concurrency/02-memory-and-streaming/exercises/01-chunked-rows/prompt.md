Write the generator function `read_in_chunks(path, size)`.

It reads a CSV file (with a header) and yields **lists of dict rows**, `size` rows per list. The last list may be shorter. An empty file (header only) yields nothing. Raise `ValueError` if `size < 1` (at the point the generator is first advanced is fine).

```python
for batch in read_in_chunks("orders.csv", 500):
    process(batch)          # at most 500 rows in memory at once
```

It must be a real generator that reads lazily, never loading the whole file first.
