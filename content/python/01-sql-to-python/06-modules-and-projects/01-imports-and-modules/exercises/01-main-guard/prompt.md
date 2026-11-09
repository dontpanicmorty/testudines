`solution.py` is a small helper that another job imports to reuse `summarize`. Since someone added a quick check at the bottom, every import prints a line into that job's logs.

Fix it so that:

- `import solution` prints **nothing**,
- running `python solution.py` still prints `3 rows, total 60`,
- `summarize` keeps working.

```python
from solution import summarize
print(summarize([1, 2]))   # 2 rows, total 3
```
