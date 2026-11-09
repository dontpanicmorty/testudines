def tally(text, letter):
    count = 0
    for ch in text.lower():
        if ch == letter.lower():
            count += 1
    return count
