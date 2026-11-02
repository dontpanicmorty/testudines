Stage three of the pipeline. `customer_totals(lines)` takes validated rows (`customer_id: int`, `quantity: int`, `unit_price: Decimal`, plus other keys you can ignore) and returns a list of `{"customer_id", "line_count", "revenue"}` dicts sorted by `customer_id`. `revenue` is the sum of `quantity * unit_price` as a `Decimal`.

```python
customer_totals([
    {"customer_id": 2, "quantity": 3, "unit_price": Decimal("12.50")},
    {"customer_id": 1, "quantity": 2, "unit_price": Decimal("5.00")},
])
# [{"customer_id": 1, "line_count": 1, "revenue": Decimal("10.00")},
#  {"customer_id": 2, "line_count": 1, "revenue": Decimal("37.50")}]
```
