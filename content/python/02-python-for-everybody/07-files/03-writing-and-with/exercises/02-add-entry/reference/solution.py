def add_entry(path, day, text):
    with open(path, "a", encoding="utf-8") as out:
        out.write(f"{day}: {text}\n")
