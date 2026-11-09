def longest_first(words):
    decorated = []
    for word in words:
        decorated.append((-len(word), word))
    decorated.sort()
    result = []
    for _, word in decorated:
        result.append(word)
    return result
