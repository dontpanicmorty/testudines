import re


def total_dollars(text):
    amounts = re.findall(r"\$(\d+\.\d\d)", text)
    return round(sum(float(a) for a in amounts), 2)
