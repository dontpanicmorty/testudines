`fetch_many(fetch, ids, limit)` calls the async function `fetch(id)` for each id and returns the results in input order. It is supposed to run the calls **concurrently, but with at most `limit` in flight at once** (to respect an API rate limit).

Right now the results are correct and the limit is never exceeded, but it is as slow as doing the calls one after another. Fix it. `limit < 1` must raise `ValueError`.

```python
results = await fetch_many(fetch_page, range(20), limit=5)
```
