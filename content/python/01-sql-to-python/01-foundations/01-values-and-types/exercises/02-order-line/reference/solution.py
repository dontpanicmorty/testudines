def order_line(name, qty, price):
    return f"{qty} x {name} @ ${price:,.2f} = ${qty * price:,.2f}"
