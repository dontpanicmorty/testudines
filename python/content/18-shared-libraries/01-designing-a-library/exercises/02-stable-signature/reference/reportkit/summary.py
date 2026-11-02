def summarize(rows, key, *, top_n=None):
    """Count rows per distinct value of `key`, most frequent first."""
    counts = {}
    for row in rows:
        counts[row[key]] = counts.get(row[key], 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked if top_n is None else ranked[:top_n]
