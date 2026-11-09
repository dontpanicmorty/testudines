from datetime import date, timedelta


def days_overdue(invoice_date, terms_days, today):
    due = invoice_date + timedelta(days=terms_days)
    return max(0, (today - due).days)
