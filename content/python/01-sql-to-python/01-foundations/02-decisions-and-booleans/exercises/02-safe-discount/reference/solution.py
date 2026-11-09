def apply_discount(price, discount_pct):
    if discount_pct is None or not (0 <= discount_pct <= 100):
        return price
    return round(price * (1 - discount_pct / 100), 2)
