def report(stock):
    lines = []
    for name in sorted(stock):
        lines.append(f"{name}: {stock[name]}")
    return lines
