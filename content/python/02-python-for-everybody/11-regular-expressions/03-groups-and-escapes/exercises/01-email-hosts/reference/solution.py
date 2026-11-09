import re


def hosts(text):
    return re.findall(r"[a-z0-9.]+@([a-z0-9]+(?:\.[a-z0-9]+)*)", text)
