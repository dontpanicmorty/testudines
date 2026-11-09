Write `days_overdue(invoice_date, terms_days, today)` returning how many whole days past the due date `today` is, or `0` if it is not yet overdue (due today is not overdue). `today` is passed in; never call `date.today()`.

```python
from datetime import date
days_overdue(date(2025, 6, 1), 30, date(2025, 7, 11))   # 10
days_overdue(date(2025, 6, 1), 30, date(2025, 7, 1))    # 0
```
