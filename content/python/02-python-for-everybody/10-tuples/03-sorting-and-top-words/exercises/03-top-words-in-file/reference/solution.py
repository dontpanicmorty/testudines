import string


def favourites(path, n):
    table = str.maketrans("", "", string.punctuation)
    counts = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            for word in line.lower().translate(table).split():
                counts[word] = counts.get(word, 0) + 1
    decorated = []
    for word, count in counts.items():
        decorated.append((-count, word))
    decorated.sort()
    return [(word, -negative) for negative, word in decorated[:n]]
