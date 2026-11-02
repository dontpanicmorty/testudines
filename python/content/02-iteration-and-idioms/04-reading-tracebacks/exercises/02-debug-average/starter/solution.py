MIN_AMOUNT = 0.01


def average_amount(rows):
    total = 0.0
    count = 0
    for i in range(len(rows) - 1):
        amount = rows[i]["amount"]
        if amount >= str(MIN_AMOUNT):
            total += float(amount)
            count += 1
    return round(total / count, 2)
