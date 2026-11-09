def top_n(orders, n):
    return sorted(orders, key=lambda o: o[1], reverse=True)[:n]
