def bands(scores):
    groups = {}
    for name, score in scores.items():
        if score >= 90:
            letter = "A"
        elif score >= 80:
            letter = "B"
        else:
            letter = "C"
        groups[letter] = groups.get(letter, []) + [name]
    for letter in groups:
        groups[letter].sort()
    return groups
