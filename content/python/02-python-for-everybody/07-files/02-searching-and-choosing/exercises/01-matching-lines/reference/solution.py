def lines_with_prefix(path, prefix):
    found = []
    handle = open(path, encoding="utf-8")
    for line in handle:
        line = line.rstrip()
        if line.startswith(prefix):
            found.append(line)
    handle.close()
    return found
