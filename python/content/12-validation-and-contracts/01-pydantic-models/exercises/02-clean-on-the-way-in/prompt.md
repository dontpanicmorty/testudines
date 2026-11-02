Real exports are messy. Define `CleanInvoice` (pydantic) so that validating a raw row also cleans it:

- `invoice_id: str` (stripped)
- `customer: str`: stripped, Title Case
- `amount: float | None`: accepts `"$1,234.50"`, `" 99 "`; `""`, `"N/A"` and `None` become `None`
- `status`: one of `"paid"`, `"open"`, `"overdue"`, `"unknown"`; input is stripped and lowercased, and an empty/missing value becomes `"unknown"` (default `"unknown"` when the key is absent)

`parse_clean(row)` returns a `CleanInvoice` from a raw dict. Garbage that cannot be cleaned (e.g. amount `"abc"`, status `"lost"`) raises `ValidationError`.
