def tidy_copy(source, target):
    written = 0
    with open(source, encoding="utf-8") as src, open(target, "w", encoding="utf-8") as dst:
        for line in src:
            line = line.strip()
            if line == "":
                continue
            dst.write(line + "\n")
            written += 1
    return written
