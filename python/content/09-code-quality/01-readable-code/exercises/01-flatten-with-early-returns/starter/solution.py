"""Order classification."""


def classify_order(order):
    if order is not None:
        if order.get("status") == "complete":
            if order.get("total", 0) > 0:
                if order.get("country") == "US":
                    return "domestic"
                else:
                    return "international"
            else:
                return "empty"
        else:
            return "open"
    else:
        return "missing"
