"""Order cleaning."""


def is_valid(order):
    return order["status"] != "cancelled" and order["total"] > 0


def clean(orders):
    return [order for order in orders if is_valid(order)]
