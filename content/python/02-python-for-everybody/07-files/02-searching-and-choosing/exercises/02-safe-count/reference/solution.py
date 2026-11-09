def count_word_lines(path, word):
    try:
        handle = open(path, encoding="utf-8")
    except FileNotFoundError:
        return None
    count = 0
    for line in handle:
        if word in line:
            count += 1
    handle.close()
    return count
