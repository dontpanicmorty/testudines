def row_total(line):
    line = line.strip()
    if line == "":
        return 0
    total = 0
    for piece in line.split(","):
        total += int(piece)
    return total
