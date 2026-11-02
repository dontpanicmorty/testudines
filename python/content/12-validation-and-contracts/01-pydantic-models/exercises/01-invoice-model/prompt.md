Define a pydantic model `Invoice` with fields `invoice_id` (str), `customer` (str), `amount` (float, must be `>= 0`) and `status` (one of `"paid"`, `"open"`, `"overdue"`). Write `parse_invoice(row)` that takes a dict of **strings** (like a CSV row, possibly with extra keys) and returns an `Invoice`. Invalid rows raise `pydantic.ValidationError`.

```python
parse_invoice({"invoice_id": "INV-1", "customer": "Ada", "amount": "12.50", "status": "paid"})
# Invoice(invoice_id='INV-1', customer='Ada', amount=12.5, status='paid')
```
