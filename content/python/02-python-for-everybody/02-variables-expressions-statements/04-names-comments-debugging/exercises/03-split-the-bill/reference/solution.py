def each_pays(bill, tip_percent, people):
    tip = bill * tip_percent / 100
    total = bill + tip
    return total / people
