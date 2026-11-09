Write `parse_amount(text)` returning a `Decimal`, or `None` when the amount is missing (blank, whitespace only, `N/A` in any case). Strip `$`, thousands commas and whitespace. Anything else that cannot be parsed raises `ValueError`.

```python
parse_amount("$3,291.26")   # Decimal("3291.26")
parse_amount(" 1310.11 ")   # Decimal("1310.11")
parse_amount("n/a")         # None
parse_amount("12 dollars")  # ValueError
```
