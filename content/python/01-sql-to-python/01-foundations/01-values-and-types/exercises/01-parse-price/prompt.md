Invoice exports store amounts as text like `"$1,234.50"` or `"  99.00 "`.

Write `parse_price(text)` that returns the amount as a **float**.

```python
parse_price("$1,234.50")   # 1234.5
parse_price("  99.00 ")    # 99.0
```

Edit `solution.py`, then press **Check**.
