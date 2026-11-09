Write `top_regions(customers, n)`: customers is a list of dicts with an optional `region`. Count customers per region (ignore rows where `region` is missing, `None` or blank, and treat regions case-insensitively, stripped, reporting them uppercase). Return the top `n` as a list of `(region, count)` tuples, highest count first, ties broken alphabetically.

```python
cs = [{"region": "eu"}, {"region": "EU "}, {"region": "us"}, {"region": None}, {}, {"region": "apac"}, {"region": "US"}]
top_regions(cs, 2)   # [("EU", 2), ("US", 2)]
top_regions(cs, 5)   # [("EU", 2), ("US", 2), ("APAC", 1)]
```
