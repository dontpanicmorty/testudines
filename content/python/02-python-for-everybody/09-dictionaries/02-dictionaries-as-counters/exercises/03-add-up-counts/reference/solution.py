def combine(first, second):
    totals = dict(first)
    for fruit in second:
        totals[fruit] = totals.get(fruit, 0) + second[fruit]
    return totals
