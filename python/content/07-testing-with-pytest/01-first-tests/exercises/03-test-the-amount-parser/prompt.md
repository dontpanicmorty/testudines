Exports from the billing system contain amounts like `$1,234.50`, `(12.00)` for negatives, blanks and `N/A`. `amounts.parse_amount(raw)` turns them into numbers:

- `"42"`, `"$42"`, `" 1,234.50 "` become floats (`42.0`, `42.0`, `1234.5`);
- an amount wrapped in parentheses is negative: `"(12.00)"` becomes `-12.0`;
- `None`, a blank string, and `"N/A"` in any letter case become `None`;
- text that is not an amount (e.g. `"abc"`) raises `ValueError`.

Write `my_tests.py` so that it passes on the real parser and fails on every hidden-bug variant. Cover each rule of the contract at least once.

```python
from amounts import parse_amount
parse_amount("$1,234.50")   # 1234.5
parse_amount("(12.00)")     # -12.0
parse_amount("N/A")         # None
```
