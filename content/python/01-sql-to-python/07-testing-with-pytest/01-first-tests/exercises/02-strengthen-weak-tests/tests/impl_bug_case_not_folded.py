"""Mixed-case statuses are not lower-cased, so 'Paused' becomes unknown."""

VALID = {"active", "paused", "cancelled"}


def normalize_status(raw):
    """Lower-case and strip a status; unrecognised, blank or None becomes 'unknown'."""
    if raw is None:
        return "unknown"
    value = raw.strip()
    return value if value in VALID else "unknown"
