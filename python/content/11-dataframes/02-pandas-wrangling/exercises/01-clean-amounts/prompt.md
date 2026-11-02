Write `clean_amounts(s)` taking a Series of strings like `"$3,291.26"`, `" 99.00 "`, `"N/A"`, `""` (or missing) and returning a **float** Series (same index) where unparseable or missing entries are `NaN`. Do not turn missing into 0.

```python
clean_amounts(pd.Series(["$1,000.50", " 7 ", "N/A", ""])).tolist()   # [1000.5, 7.0, nan, nan]
```
