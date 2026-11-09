from collections import Counter


def top_regions(customers, n):
    counts = Counter(
        c["region"].strip().upper()
        for c in customers
        if c.get("region") and c["region"].strip()
    )
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
