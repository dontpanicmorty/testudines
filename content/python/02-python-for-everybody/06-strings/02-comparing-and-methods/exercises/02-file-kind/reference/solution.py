def file_kind(filename):
    name = filename.lower()
    if name.endswith(".py"):
        return "python"
    if name.endswith(".txt") or name.endswith(".md"):
        return "text"
    if name.endswith(".csv"):
        return "table"
    return "unknown"
