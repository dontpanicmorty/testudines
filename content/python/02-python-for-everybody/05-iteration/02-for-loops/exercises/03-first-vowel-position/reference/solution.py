def first_vowel_index(text):
    for i in range(len(text)):
        if text[i] in "aeiouAEIOU":
            return i
    return -1
