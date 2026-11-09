import re


def grep(path, pattern):
    found = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if re.search(pattern, line):
                found.append(line)
    return found
