A table is a list of rows, and each row is a list of values. Write `columns_of(rows)` that returns the table's columns as a list of lists, so the first inner list holds the first item of every row, and so on.

```python
columns_of([[1, 2, 3], [4, 5, 6]])    # [[1, 4], [2, 5], [3, 6]]
```

An empty table gives `[]`. If the rows are not all the same length, raise a `ValueError`.
