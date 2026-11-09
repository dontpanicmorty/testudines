def line_count(path):
    count = 0
    handle = open(path, encoding="utf-8")
    for line in handle:
        count += 1
    handle.close()
    return count
