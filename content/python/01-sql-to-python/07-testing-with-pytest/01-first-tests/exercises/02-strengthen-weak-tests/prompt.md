`status.py` normalises subscription statuses coming from several systems:

- strips surrounding whitespace and lower-cases the value;
- `"active"`, `"paused"` and `"cancelled"` are the only recognised statuses;
- anything else, a blank string, or `None` becomes `"unknown"`.

A teammate wrote `my_tests.py`. It's green, and yet a refactor shipped a bug last week without a single test going red. Rewrite the tests so that they would have caught it: they must still pass on the real function but fail on each buggy variant.

```python
from status import normalize_status
normalize_status("  Paused ")   # "paused"
normalize_status(None)          # "unknown"
normalize_status("archived")    # "unknown"
```

Keep at least 4 tests.
