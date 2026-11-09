Write two functions.

`make_request_url(base, params, environ)` returns the request address for a keyed service. The key is stored in `environ["PLACE_API_KEY"]` (`environ` is a dictionary like `os.environ`). Return `base + "?" + query`, where the query is the escaped `params` followed by `key=<the key>`. If the key is missing, raise `RuntimeError`. Do not fetch anything.

`collect_items(first_url)` fetches `first_url` (JSON like `{"items": [...], "next": "<address or null>"}`), then keeps following `next` until it is null, and returns all the items in one list.

```python
make_request_url("http://x.test/a", {"q": "oak"}, {"PLACE_API_KEY": "k1"})
# "http://x.test/a?q=oak&key=k1"
```
