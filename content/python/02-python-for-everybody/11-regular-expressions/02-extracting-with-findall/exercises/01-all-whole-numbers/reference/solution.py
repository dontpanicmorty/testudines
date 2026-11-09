import re


def numbers_in(text):
    return [int(piece) for piece in re.findall(r"\d+", text)]
