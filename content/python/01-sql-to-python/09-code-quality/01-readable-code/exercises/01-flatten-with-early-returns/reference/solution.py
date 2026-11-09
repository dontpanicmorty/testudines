"""Order classification."""


def classify_order(order):
    if order is None:
        return "missing"
    if order.get("status") != "complete":
        return "open"
    if order.get("total", 0) <= 0:
        return "empty"
    if order.get("country") == "US":
        return "domestic"
    return "international"
