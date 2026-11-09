def classify_order(row):
    if row is None or not isinstance(row.get("status"), str):
        return "invalid"
    status = row["status"].strip().lower()
    if status in ("cancelled", "returned"):
        return "closed"
    amount = row.get("amount")
    if amount is None or amount <= 0:
        return "unpaid"
    if status in ("shipped", "delivered"):
        return "fulfilled"
    return "open"
