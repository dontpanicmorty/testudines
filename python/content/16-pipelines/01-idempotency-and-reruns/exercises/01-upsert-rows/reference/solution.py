def upsert(existing, incoming, key):
    by_key = {row[key]: row for row in existing}
    for row in incoming:
        by_key[row[key]] = row
    return list(by_key.values())
