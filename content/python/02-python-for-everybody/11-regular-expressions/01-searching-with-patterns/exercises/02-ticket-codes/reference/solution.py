import re


def is_ticket(text):
    return re.search(r"^[A-Z][A-Z]-\d+$", text) is not None
