`reportkit.summarize(rows, key)` returns `(value, count)` pairs sorted by count descending, then value ascending. Dozens of pipelines call it. Analysts now want only the top few.

Add a `top_n` option such that:

- every existing call (`summarize(rows, "region")`) behaves exactly as before,
- `summarize(rows, "region", top_n=2)` returns at most 2 pairs,
- `top_n` is **keyword-only** (passing it positionally must raise `TypeError`),
- `top_n=0` returns an empty list, and `top_n=None` (the default) returns everything.

```python
from reportkit import summarize
summarize(rows, "region", top_n=1)   # [("eu", 2)]
```
