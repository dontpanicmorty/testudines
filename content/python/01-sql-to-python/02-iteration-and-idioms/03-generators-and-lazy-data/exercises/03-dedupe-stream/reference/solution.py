def dedupe(rows, key):
    seen = set()
    for row in rows:
        k = key(row)
        if k in seen:
            continue
        seen.add(k)
        yield row
