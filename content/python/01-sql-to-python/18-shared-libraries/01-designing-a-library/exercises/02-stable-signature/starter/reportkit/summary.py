def summarize(rows, key):
    """Count rows per distinct value of `key`, most frequent first."""
    counts = {}
    for row in rows:
        counts[row[key]] = counts.get(row[key], 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
