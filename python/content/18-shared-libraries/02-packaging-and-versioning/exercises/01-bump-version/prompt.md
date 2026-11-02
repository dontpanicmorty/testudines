Write `bump(version, part)` where `part` is `"major"`, `"minor"` or `"patch"`.

Also write `is_newer(a, b)` returning `True` when version `a` is strictly newer than `b`. Compare numerically, not as text.

```python
bump("1.4.2", "minor")      # "1.5.0"
bump("1.4.2", "major")      # "2.0.0"
bump("1.4.9", "patch")      # "1.4.10"
is_newer("1.10.0", "1.9.0") # True
```

An unknown `part` or a version that is not three dot-separated integers raises `ValueError`.
