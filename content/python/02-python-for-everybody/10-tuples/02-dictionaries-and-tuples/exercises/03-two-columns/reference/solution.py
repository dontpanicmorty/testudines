def columns(d):
    keys = sorted(d)
    values = []
    for key in keys:
        values.append(d[key])
    return (keys, values)
