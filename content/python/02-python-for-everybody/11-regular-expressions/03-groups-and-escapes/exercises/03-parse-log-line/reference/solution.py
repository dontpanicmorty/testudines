import re


def parse_line(line):
    m = re.search(r"^(\d\d\d\d-\d\d-\d\d) (\d\d:\d\d:\d\d) \[([A-Z]+)\] (.+)$", line)
    if not m:
        return None
    return {"date": m.group(1), "time": m.group(2), "level": m.group(3), "message": m.group(4)}
