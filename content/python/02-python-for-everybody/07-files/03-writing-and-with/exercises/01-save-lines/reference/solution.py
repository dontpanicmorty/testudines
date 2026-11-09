def save_lines(path, items):
    with open(path, "w", encoding="utf-8") as out:
        for item in items:
            out.write(item + "\n")
