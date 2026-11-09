`messages` is a list of `(sender, date)` pairs; the sender may have a display name in angle brackets, odd capitals or extra spaces, and the date looks like `"2026-01-14"`.

Write `activity(messages)` returning a dictionary with two lists:

- `"by_org"`: `(organization, count)` pairs, biggest count first, ties alphabetical. The organization is the last two dot-separated parts of the sender's domain (the text after `@`), lowercased.
- `"by_month"`: `(month, count)` pairs sorted by month, where month is the first seven characters of the date.

```python
activity([("A <a@mail.x.org>", "2026-01-02"), ("b@X.org", "2026-02-01")])
# {"by_org": [("x.org", 2)], "by_month": [("2026-01", 1), ("2026-02", 1)]}
```
