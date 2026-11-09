def tally(votes):
    counts = {}
    for name in votes:
        counts[name] = counts.get(name, 0) + 1
    return counts
