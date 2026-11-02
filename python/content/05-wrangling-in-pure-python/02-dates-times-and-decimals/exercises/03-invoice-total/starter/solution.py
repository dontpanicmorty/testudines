def invoice_total(lines, tax_rate):
    subtotal = 0.0
    for qty, price in lines:
        subtotal += qty * float(price)
    total = subtotal * (1 + float(tax_rate))
    return round(total, 2)
