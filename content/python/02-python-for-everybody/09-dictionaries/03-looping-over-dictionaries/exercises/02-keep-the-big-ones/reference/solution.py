def at_least(counts, minimum):
    kept = {}
    for key, value in counts.items():
        if value >= minimum:
            kept[key] = value
    return kept
