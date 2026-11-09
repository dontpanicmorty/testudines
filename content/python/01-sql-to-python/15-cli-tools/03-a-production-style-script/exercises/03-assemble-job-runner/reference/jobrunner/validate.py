VALID_STATUSES = {"open", "shipped", "cancelled"}


def validate_row(row: dict) -> list[str]:
    """Return a list of problems; an empty list means the row is valid."""
    problems: list[str] = []
    try:
        if int(str(row.get("order_id", "")).strip()) <= 0:
            problems.append("order_id: must be positive")
    except ValueError:
        problems.append("order_id: not an integer")
    try:
        if float(str(row.get("amount", "")).strip()) < 0:
            problems.append("amount: must not be negative")
    except ValueError:
        problems.append("amount: not a number")
    status = str(row.get("status", "")).strip().lower()
    if status not in VALID_STATUSES:
        problems.append(f"status: unknown value {status!r}")
    return problems
