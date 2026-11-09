dbt packages and Python libraries use versions like `1.10.2`. Sorting them as text puts `1.10` before `1.9`. Implement `Version` as a frozen, orderable dataclass.

- fields `major: int`, `minor: int = 0`, `patch: int = 0`;
- `Version.parse(text)` accepts `"1"`, `"1.2"`, `"1.2.3"`, each with an optional leading `v` (missing parts are 0). Anything else (empty, non-numeric parts, more than three parts) raises `ValueError`;
- `str(version)` always shows three parts: `"1.2.3"`;
- versions sort numerically.

```python
sorted([Version.parse("1.10"), Version.parse("v1.9.1"), Version.parse("1")])
str(Version.parse("v2.1"))     # '2.1.0'
Version.parse("1.x")           # raises ValueError
```
