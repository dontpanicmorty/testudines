Write `total_dollars(text)` that finds every price written like `$12.50` (a dollar sign, one or more digits, a dot, exactly two digits) and returns their sum as a float, rounded to 2 decimal places. Anything else, such as `12.50` without a dollar sign or `$7` without cents, is ignored. If there are no prices return `0.0`.

```python
total_dollars("tea $3.50 and cake $4.25, tip 2.00, gum $1")    # 7.75
```
