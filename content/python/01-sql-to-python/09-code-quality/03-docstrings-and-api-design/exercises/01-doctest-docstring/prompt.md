Implement `parse_duration(text)` and give it a proper docstring.

Behaviour: `text` is one or more `<digits><unit>` parts with units `d` (86400 s), `h` (3600), `m` (60) and `s` (1), e.g. `"1h30m"` is 5400, `"2d"` is 172800, `"90s"` is 90. Surrounding whitespace is ignored. Anything else (empty, no unit, unknown unit, stray characters) raises `ValueError`.

The docstring must:

- start with a one-line summary,
- have `Args:`, `Returns:` and `Raises:` sections (Google style),
- include an `Examples:` block of **at least three** doctests that really pass (they are executed).

```python
parse_duration("1h30m")   # 5400
parse_duration("45s")     # 45
parse_duration("abc")     # raises ValueError
```
