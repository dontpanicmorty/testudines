def flip(pairs):
    result = []
    for first, second in pairs:
        result.append((second, first))
    return result
