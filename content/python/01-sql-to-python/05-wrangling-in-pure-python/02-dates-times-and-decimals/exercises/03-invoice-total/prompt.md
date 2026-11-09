`invoice_total(lines, tax_rate)` takes `lines` as `(quantity: int, unit_price: str)` tuples and `tax_rate` as a string like `"0.0825"`. It must return the total **including tax** as a `Decimal` with exactly two decimal places, rounded half up, with the rounding done once on the grand total.

Currently the totals drift by a cent in some cases (and the result is a float). Fix it.

```python
invoice_total([(3, "0.10")], "0")                  # Decimal("0.30")
invoice_total([(1, "2.675")], "0")                 # Decimal("2.68")
invoice_total([(2, "19.99"), (1, "5.00")], "0.0825")   # Decimal("48.69")
```
