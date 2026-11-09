def merge_tables(a, b):
    merged = []
    for row in a + b:
        merged.append(row[:])
    return merged
