import re


def quoted(text):
    pieces = re.findall(r'".*?"', text)
    return [piece[1:-1] for piece in pieces]
