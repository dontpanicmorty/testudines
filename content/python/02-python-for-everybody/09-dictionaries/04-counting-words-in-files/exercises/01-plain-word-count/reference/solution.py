def count_words(path):
    counts = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            for word in line.split():
                counts[word] = counts.get(word, 0) + 1
    return counts
