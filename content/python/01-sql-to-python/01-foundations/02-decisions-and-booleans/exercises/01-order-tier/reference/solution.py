def order_tier(amount):
    if amount >= 1000:
        return "enterprise"
    if amount >= 100:
        return "standard"
    if amount > 0:
        return "small"
    return "none"
