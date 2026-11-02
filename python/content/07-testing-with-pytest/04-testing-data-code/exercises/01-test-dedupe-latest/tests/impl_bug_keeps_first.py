"""The first row seen wins instead of the latest."""


def dedupe_latest(rows):
    """One row per id: greatest updated_at wins (None oldest, ties: later row). Sorted by id."""
    best = {}
    for row in rows:
        current = best.get(row["id"])
        if current is None:
            best[row["id"]] = row
    return [best[key] for key in sorted(best)]
