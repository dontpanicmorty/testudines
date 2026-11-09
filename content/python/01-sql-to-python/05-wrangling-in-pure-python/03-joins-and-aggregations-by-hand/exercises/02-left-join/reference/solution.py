def left_join(left, right, on, right_columns):
    lookup = {}
    for r in right:
        lookup.setdefault(r[on], []).append(r)
    out = []
    for row in left:
        matches = lookup.get(row[on])
        if matches:
            for m in matches:
                out.append({**row, **{c: m[c] for c in right_columns}})
        else:
            out.append({**row, **{c: None for c in right_columns}})
    return out
