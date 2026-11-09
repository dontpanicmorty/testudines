def add_tax(price, tax_percent):
    return price * (1 + tax_percent / 100)


def add_delivery(amount, delivery):
    return amount + delivery


def final_total(price, tax_percent, delivery):
    taxed = add_tax(price, tax_percent)
    return add_delivery(taxed, delivery)
