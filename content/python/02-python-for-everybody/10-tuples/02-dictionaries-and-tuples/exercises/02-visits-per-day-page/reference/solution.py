def visit_counts(log):
    counts = {}
    for entry in log:
        counts[entry] = counts.get(entry, 0) + 1
    return counts
