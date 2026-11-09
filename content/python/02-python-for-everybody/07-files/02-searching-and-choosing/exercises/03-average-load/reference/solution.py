def average_load(path):
    total = 0.0
    count = 0
    handle = open(path, encoding="utf-8")
    for line in handle:
        line = line.rstrip()
        if not line.startswith("LOAD "):
            continue
        total += float(line.split()[1])
        count += 1
    handle.close()
    if count == 0:
        return None
    return total / count
