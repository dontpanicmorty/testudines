Write `build_url(base, params)` that returns the full request address: the base, then `?`, then the parameters as a properly escaped query string, in the dictionary's order. If `params` is empty, return `base` unchanged (no `?`).

```python
build_url("http://x.test/find", {"q": "red bike", "n": 3})
# "http://x.test/find?q=red+bike&n=3"
```
