Write the generator `batched(items, size)` that yields **lists** of at most `size` items from any iterable, in order. The last batch may be shorter. It must not consume more of the input than needed (it works on infinite streams), and `size < 1` raises `ValueError`.

```python
list(batched(range(7), 3))   # [[0, 1, 2], [3, 4, 5], [6]]
list(batched([], 3))         # []
```
