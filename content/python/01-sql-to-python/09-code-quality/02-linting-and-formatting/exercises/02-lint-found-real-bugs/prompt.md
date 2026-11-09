Two functions in `solution.py` are flagged by ruff's bugbear rules (`B006`, `B023`), and both warnings point at genuine bugs:

- `add_tag(tag, tags=[])`: calling `add_tag("a")` and later `add_tag("b")` returns lists that share state, so the second result contains both tags. It should return `["b"]`. When a list **is** passed, the tag is appended to that list and the same list is returned.
- `make_filters(thresholds)` returns one predicate per threshold, each answering "is `row['value'] >= threshold`?". Right now every predicate uses the *last* threshold.

Fix both so behaviour is correct and `python -m ruff check --select B,E,F solution.py` is clean (no `# noqa`).

```python
add_tag("a")                        # ['a']
add_tag("b")                        # ['b']
low, high = make_filters([10, 50])
low({"value": 20}), high({"value": 20})   # (True, False)
```
