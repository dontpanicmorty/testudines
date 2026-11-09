Write `assert_matches_golden(actual, golden_path, *, update=False)`, the helper a team shares for golden-file tests.

- With `update=True`: write `actual` to `golden_path` (creating parent folders) and return `None`. This is how a reviewed change is accepted.
- Otherwise, if the golden file **doesn't exist**, raise `AssertionError` with a message that mentions `update=True`. A missing golden must never pass silently.
- Otherwise compare the file's text with `actual`. If equal, return `None`. If different, raise `AssertionError` whose message contains a unified diff: lines of the golden text prefixed `-` and lines of the actual text prefixed `+`.

```python
assert_matches_golden("EU 17\n", "goldens/report.txt", update=True)  # writes the file
assert_matches_golden("EU 18\n", "goldens/report.txt")
# AssertionError: ... -EU 17 ... +EU 18
```
