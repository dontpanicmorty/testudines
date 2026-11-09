def apply_corrections(rows, fixes):
    result = list(rows)
    for index, field, value in fixes:
        result[index][field] = value
    return result
