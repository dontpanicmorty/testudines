def read_clean(path):
    lines = []
    handle = open(path, encoding="utf-8")
    for line in handle:
        lines.append(line.rstrip("\n"))
    handle.close()
    return lines
