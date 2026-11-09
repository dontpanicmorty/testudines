def starting_letters(words):
    counts = {}
    for word in words:
        if word == "":
            continue
        letter = word[0].lower()
        counts[letter] = counts.get(letter, 0) + 1
    return counts
