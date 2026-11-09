def priciest(prices):
    best = None
    for name, price in prices.items():
        if best is None or price > best[1] or (price == best[1] and name < best[0]):
            best = (name, price)
    return best
