def rows_as_dicts(cur):
    if cur.description is None:
        return []
    names = [col[0].lower() for col in cur.description]
    out = []
    record = {}
    for row in cur.fetchall():
        for i, name in enumerate(names):
            record[name] = row[i]
        out.append(record)
    return out
