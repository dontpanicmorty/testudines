import re


def is_alarm(line):
    return re.search(r"^ERROR:", line) is not None
