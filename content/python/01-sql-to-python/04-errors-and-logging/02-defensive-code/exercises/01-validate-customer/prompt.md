`validate_customer(raw)` takes a dict from a CSV row and returns a clean dict, or raises `ValidationError` (a `ValueError` subclass, already defined) listing **every** problem joined with `"; "`.

Rules: `customer_id` must be a positive integer (returned as `int`); `email` is stripped and lowercased and must contain exactly one `@`; `plan` must be one of `free`, `pro`, `team` (compared case-insensitively, returned lowercase).

```python
validate_customer({"customer_id": "5", "email": " A@B.com ", "plan": "PRO"})
# {"customer_id": 5, "email": "a@b.com", "plan": "pro"}
```
