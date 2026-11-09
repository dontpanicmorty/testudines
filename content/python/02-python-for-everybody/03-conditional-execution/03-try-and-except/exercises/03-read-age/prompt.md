A form field gives you an age as text. Write `parse_age(text)` that returns the age as a whole number if the text is a whole number from 0 to 120 inclusive. In every other case (not a number, a decimal, negative, or over 120) return `None`.

```python
parse_age("34")     # 34
parse_age("old")    # None
parse_age("-5")     # None
parse_age("200")    # None
```
