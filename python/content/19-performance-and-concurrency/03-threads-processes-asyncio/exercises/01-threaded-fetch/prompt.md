Write `fetch_all(fetch, ids, max_workers=8)`.

`fetch` is a blocking function taking one id and returning a result (think: an API call). Call it for every id **concurrently on a thread pool** and return the list of results **in the same order as `ids`**.

- If any call raises, the exception propagates to the caller.
- `max_workers < 1` raises `ValueError`.
- An empty `ids` list returns `[]`.

```python
fetch_all(get_page, [1, 2, 3], max_workers=3)   # [page1, page2, page3]
```
