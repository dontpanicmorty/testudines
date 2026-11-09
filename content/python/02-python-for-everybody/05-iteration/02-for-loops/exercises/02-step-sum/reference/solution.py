def sum_stepped(start, stop, step):
    total = 0
    for n in range(start, stop, step):
        total += n
    return total
