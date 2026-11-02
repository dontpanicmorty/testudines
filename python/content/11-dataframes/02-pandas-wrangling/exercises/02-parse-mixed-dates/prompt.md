Invoice dates arrive as `2025-09-26`, `05/26/2025` (month first) or `20 Jun 2025`. Write `parse_dates(s)` returning a datetime Series (same index) with `NaT` for anything that fits none of the three formats or is missing. It must be deterministic: `03/04/2025` is March 4th.

```python
parse_dates(pd.Series(["2025-09-26", "05/26/2025", "20 Jun 2025", "oops"]))
# 2025-09-26, 2025-05-26, 2025-06-20, NaT
```
