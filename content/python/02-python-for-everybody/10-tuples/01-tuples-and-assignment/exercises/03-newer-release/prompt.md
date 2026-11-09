Version labels look like `"1.10.2"`: whole numbers separated by dots. Write `compare_versions(a, b)` that returns `-1` if `a` is an older release than `b`, `1` if `a` is newer, and `0` if they are the same. Compare the numbers, not the text, so `"1.10"` is newer than `"1.9"`. If one label is a prefix of the other, the longer one is newer (`"2.0"` is older than `"2.0.1"`).

```python
compare_versions("1.10", "1.9")    # 1
compare_versions("2.0", "2.0")     # 0
```
