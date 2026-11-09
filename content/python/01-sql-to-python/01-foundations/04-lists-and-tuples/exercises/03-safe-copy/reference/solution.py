def apply_corrections(rows, fixes):
    result = [dict(row) for row in rows]
    for index, field, value in fixes:
        result[index][field] = value
    return result
