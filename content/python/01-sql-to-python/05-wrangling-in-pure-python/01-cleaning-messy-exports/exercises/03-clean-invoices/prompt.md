Write `clean_invoices(path)` that reads a messy invoice CSV and returns a list of dicts with exactly these keys:

- `invoice_id` (str, stripped)
- `customer` (str, stripped, `.title()`)
- `amount` (`Decimal` or `None` when missing / `N/A`; strip `$` and commas)
- `invoice_date` (`datetime.date`; formats `YYYY-MM-DD`, `20 Jun 2025`, `05/26/2025` month-first)
- `status` (lowercase str, or `None` if blank)

Source headers are messy (`"Invoice #"`, `"Customer Name "`, `"AMOUNT"`, `"Invoice Date"`, `"Status"`): normalise them yourself. Rows repeated by `invoice_id` are dropped (first wins); order is preserved. This is a from-scratch exercise: design the helpers yourself.

```python
clean_invoices(Path("messy_invoices.csv"))[0]
# {"invoice_id": "INV-0001", "customer": "Margaret Liskov", "amount": Decimal("1310.11"),
#  "invoice_date": date(2025, 9, 26), "status": "paid"}
```
