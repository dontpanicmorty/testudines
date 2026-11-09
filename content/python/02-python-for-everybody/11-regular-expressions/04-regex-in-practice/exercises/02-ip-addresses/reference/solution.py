import re


def addresses(path):
    found = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            found.extend(re.findall(r"\d+\.\d+\.\d+\.\d+", line))
    return found
