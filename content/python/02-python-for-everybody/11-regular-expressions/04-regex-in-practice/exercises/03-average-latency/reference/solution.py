import re


def average_ms(path):
    total = 0
    count = 0
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            m = re.search(r"took (\d+) ms", line)
            if m:
                total += int(m.group(1))
                count += 1
    if count == 0:
        return 0.0
    return total / count
