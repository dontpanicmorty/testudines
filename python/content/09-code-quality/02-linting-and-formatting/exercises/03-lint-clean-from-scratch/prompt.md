Write `normalize_headers(headers)` that turns messy CSV headers into safe column names, **and** keep the file clean under both checks the team runs in CI:

```
python -m ruff check --select E,F,I,B,UP,SIM,N,C4 solution.py
python -m ruff format --check solution.py
```

(default formatting: 88 columns, double quotes). Rules for the names:

1. strip, lower-case, and turn every run of non-alphanumeric characters into a single `_`; trim leading/trailing `_`;
2. an empty result becomes `col_<index>` (zero-based position in the list);
3. if a name repeats, later occurrences get `_2`, `_3`... in order.

```python
normalize_headers(["Order ID", " Total ($) ", "total", "", "TOTAL"])
# ['order_id', 'total', 'total_2', 'col_3', 'total_3']
```
