Bulk inserts work best in chunks. Write a generator `batches(iterable, size)` that yields lists of up to `size` items, in order. The last batch may be shorter. It must work on any iterable (including generators and infinite streams) without loading it all, and raise `ValueError` if `size < 1`.

```python
list(batches(range(7), 3))   # [[0, 1, 2], [3, 4, 5], [6]]
list(batches([], 3))         # []
```
