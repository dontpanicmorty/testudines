def collect_words(items):
    kept = []
    i = 0
    while i < len(items):
        word = items[i]
        i += 1
        if word == "":
            continue
        if word == "STOP":
            break
        kept.append(word)
    return kept
