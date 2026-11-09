def group_totals(rows, key, value):
    out = {}
    for r in rows:
        g = out.setdefault(r[key], {"count": 0, "total": 0})
        g["count"] += 1
        if r[value] is not None:
            g["total"] += r[value]
    return out
