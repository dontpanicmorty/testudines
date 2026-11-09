"""Small helpers that need type hints."""


def total_cents(prices):
    return sum(round(p * 100) for p in prices)


def first_or_none(items):
    return items[0] if items else None


def group_by_region(rows):
    groups = {}
    for row in rows:
        groups.setdefault(row["region"], []).append(row["customer_id"])
    return groups
