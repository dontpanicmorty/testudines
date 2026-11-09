The `pricing` library has a pure function `net_price(gross, vat_rate)` and an optional helper `to_frame(items)` that returns a pandas DataFrame. A consumer running in a minimal container (no pandas installed) reports:

```
ImportError: No module named 'pandas'
```

...just from `import pricing`, even though they never call `to_frame`.

Fix the library so that:

- `import pricing` and `pricing.net_price(...)` work when pandas is not importable (and must not import pandas as a side effect),
- `pricing.to_frame(items)` still returns a DataFrame with columns `sku`, `gross`, `net` when pandas is available.

```python
import pricing
pricing.net_price(120.0, 0.2)          # 100.0
pricing.to_frame([("a", 120.0, 0.2)])  # DataFrame with columns sku, gross, net
```
