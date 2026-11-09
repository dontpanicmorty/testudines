import re


def first_integer(text):
    m = re.search(r"-?\d+", text)
    if m:
        return int(m.group())
    return None
