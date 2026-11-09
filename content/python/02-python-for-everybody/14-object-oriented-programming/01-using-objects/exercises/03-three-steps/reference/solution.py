def read_rows(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        name, minutes = line.split(",")
        rows.append((name, int(minutes)))
    return rows


def totals(rows):
    result = {}
    for name, minutes in rows:
        result[name] = result.get(name, 0) + minutes
    return result


def format_totals(result):
    ordered = sorted(result.items(), key=lambda item: (-item[1], item[0]))
    return "\n".join(f"{name}: {minutes}" for name, minutes in ordered)


def report(text):
    return format_totals(totals(read_rows(text)))
