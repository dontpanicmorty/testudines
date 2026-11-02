MIN_AMOUNT = 0.01


def average_amount(rows):
    total = 0.0
    count = 0
    for row in rows:
        amount = float(row["amount"])
        if amount >= MIN_AMOUNT:
            total += amount
            count += 1
    if count == 0:
        return 0.0
    return round(total / count, 2)
