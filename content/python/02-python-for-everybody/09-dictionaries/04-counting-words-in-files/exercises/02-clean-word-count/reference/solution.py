import string


def word_frequencies(path):
    table = str.maketrans("", "", string.punctuation)
    counts = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.lower().translate(table)
            for word in line.split():
                counts[word] = counts.get(word, 0) + 1
    return counts
