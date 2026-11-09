def first_failure(rows, parse):
    for i, row in enumerate(rows):
        try:
            parse(row)
        except Exception as exc:
            return i, type(exc).__name__, str(exc)
    return None
