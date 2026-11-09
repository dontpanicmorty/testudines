def receipt_line(item, qty, price):
    total = qty * price
    return f"{item:<10} x{qty} {total:>8.2f}"
