def total_stock(path):
    total = 0
    handle = open(path, encoding="utf-8")
    for line in handle:
        line = line.strip()
        if line == "":
            continue
        name, amount = line.split()
        total += int(amount)
    handle.close()
    return total
