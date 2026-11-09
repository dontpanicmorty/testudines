def in_both(first, second):
    names = []
    for name in first:
        if name in second:
            names.append(name)
    return sorted(names)
