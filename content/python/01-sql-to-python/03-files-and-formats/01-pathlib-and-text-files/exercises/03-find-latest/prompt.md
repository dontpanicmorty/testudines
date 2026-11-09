Exports land as `orders_<n>.csv` where `n` is a growing batch number (`orders_9.csv`, `orders_10.csv`, ...). `latest_export(folder)` should return the `Path` with the **highest batch number**, or `None` if the folder has no exports. Right now it returns the wrong file once batch numbers reach two digits, and it also trips on other files in the folder (like `orders_notes.txt`). Fix it.

```python
latest_export(folder)   # folder has orders_9.csv, orders_10.csv -> orders_10.csv
```
