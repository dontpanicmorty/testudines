def ticket_price(age, is_member):
    if age < 12:
        return 5
    if age >= 65:
        price = 6
    else:
        price = 10
    if is_member:
        price = price - 2
    return price
