from decimal import ROUND_HALF_UP, Decimal


def invoice_total(lines, tax_rate):
    subtotal = Decimal("0")
    for qty, price in lines:
        subtotal += qty * Decimal(price)
    total = subtotal * (1 + Decimal(tax_rate))
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
