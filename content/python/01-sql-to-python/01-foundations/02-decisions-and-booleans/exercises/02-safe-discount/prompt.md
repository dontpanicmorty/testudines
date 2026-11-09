Write `apply_discount(price, discount_pct)`.

- `discount_pct` is a percentage from 0 to 100, or `None` when the source system had no value (treat as no discount).
- Return `price` reduced by that percentage, rounded to 2 decimals.
- If `discount_pct` is outside 0-100, return `price` unchanged (bad data must not create negative prices or price increases).

```python
apply_discount(200.0, 25)    # 150.0
apply_discount(200.0, None)  # 200.0
apply_discount(200.0, 0)     # 200.0
apply_discount(200.0, 150)   # 200.0
apply_discount(19.99, 10)    # 17.99
```
