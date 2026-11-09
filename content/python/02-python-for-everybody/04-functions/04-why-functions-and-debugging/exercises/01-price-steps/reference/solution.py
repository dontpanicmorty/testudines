def shop_price(price, discount_percent):
    reduced = price - price * discount_percent / 100
    return reduced * 1.2
