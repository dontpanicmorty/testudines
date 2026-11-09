import keyword


def is_reserved(word):
    return keyword.iskeyword(word)
