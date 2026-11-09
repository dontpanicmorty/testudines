def top_n(counts, n):
    decorated = []
    for word, count in counts.items():
        decorated.append((-count, word))
    decorated.sort()
    result = []
    for negative, word in decorated[:n]:
        result.append((word, -negative))
    return result
