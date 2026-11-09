def compare_versions(a, b):
    first = tuple(int(part) for part in a.split("."))
    second = tuple(int(part) for part in b.split("."))
    if first < second:
        return -1
    if first > second:
        return 1
    return 0
