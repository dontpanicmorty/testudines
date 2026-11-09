def longest_word(sentence):
    best = ""
    for word in sentence.split():
        if len(word) > len(best):
            best = word
    return best
