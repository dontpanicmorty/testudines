Implement a frozen dataclass `OrderLine` with fields `order_id: int`, `sku: str`, `quantity: int`, `unit_price_cents: int`.

On creation it must:

- strip whitespace from `sku` and upper-case it; a blank `sku` raises `ValueError` (message mentions `sku`);
- reject `quantity < 1` with `ValueError` (message mentions `quantity`);
- reject a negative `unit_price_cents` with `ValueError` (message mentions `unit_price_cents`).

It also has a property `total_cents` (`quantity * unit_price_cents`). Instances are immutable and hashable.

```python
line = OrderLine(7, " ab-12 ", 3, 250)
line.sku            # 'AB-12'
line.total_cents    # 750
line.quantity = 5   # raises dataclasses.FrozenInstanceError
```
