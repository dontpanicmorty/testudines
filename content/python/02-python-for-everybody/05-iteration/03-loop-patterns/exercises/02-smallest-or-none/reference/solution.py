def lowest(readings):
    smallest = None
    for r in readings:
        if smallest is None or r < smallest:
            smallest = r
    return smallest
