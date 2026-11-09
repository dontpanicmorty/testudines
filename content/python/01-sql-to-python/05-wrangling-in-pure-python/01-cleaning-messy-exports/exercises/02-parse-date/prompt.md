The invoice export mixes `2025-09-26`, `20 Jun 2025` and `05/26/2025` (month first). Write `parse_date(text)` returning a `datetime.date`. Surrounding whitespace is ignored. Any other format raises `ValueError` whose message includes the offending text.

```python
parse_date("2025-09-26")    # date(2025, 9, 26)
parse_date("20 Jun 2025")   # date(2025, 6, 20)
parse_date("05/26/2025")    # date(2025, 5, 26)
parse_date("26/05/2025")    # ValueError (there is no month 26)
```
