import string


def line_spread(path):
    table = str.maketrans("", "", string.punctuation)
    spread = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            words = line.lower().translate(table).split()
            seen = []
            for word in words:
                if word not in seen:
                    seen.append(word)
            for word in seen:
                spread[word] = spread.get(word, 0) + 1
    return spread
