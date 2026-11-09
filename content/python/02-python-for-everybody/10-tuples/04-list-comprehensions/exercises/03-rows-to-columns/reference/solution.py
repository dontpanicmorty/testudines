def columns_of(rows):
    if len(rows) == 0:
        return []
    width = len(rows[0])
    for row in rows:
        if len(row) != width:
            raise ValueError("rows have different lengths")
    return [[row[j] for row in rows] for j in range(width)]
