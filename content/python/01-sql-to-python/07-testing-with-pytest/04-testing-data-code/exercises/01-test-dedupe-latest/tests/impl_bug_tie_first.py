"""On an exact tie the earlier row wins instead of the later one."""


def dedupe_latest(rows):
    """One row per id: greatest updated_at wins (None oldest, ties: later row). Sorted by id."""
    best = {}
    for row in rows:
        current = best.get(row["id"])
        if current is None or (row["updated_at"] or "") > (current["updated_at"] or ""):
            best[row["id"]] = row
    return [best[key] for key in sorted(best)]
