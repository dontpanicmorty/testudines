def drop_all(items, bad):
    removed = 0
    i = len(items) - 1
    while i >= 0:
        if items[i] == bad:
            del items[i]
            removed += 1
        i -= 1
    return removed
