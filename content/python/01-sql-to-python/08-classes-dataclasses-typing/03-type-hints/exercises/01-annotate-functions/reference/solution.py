"""Small helpers that need type hints."""


def total_cents(prices: list[float]) -> int:
    return sum(round(p * 100) for p in prices)


def first_or_none[T](items: list[T]) -> T | None:
    return items[0] if items else None


def group_by_region(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for row in rows:
        groups.setdefault(row["region"], []).append(row["customer_id"])
    return groups
