Write `dig(json_text, path, default=None)`. It parses the JSON, then follows `path` (a list of dictionary keys and list positions) step by step and returns the value found. If any step is impossible (missing key, position out of range, or trying to go into a plain number or string), return `default`.

```python
text = '{"a": {"b": [10, 20, {"c": "deep"}]}}'
dig(text, ["a", "b", 2, "c"])          # "deep"
dig(text, ["a", "x"], "none")          # "none"
dig(text, ["a", "b", 9], -1)           # -1
```
