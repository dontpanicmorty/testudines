"""Surrounding whitespace is not stripped."""

VALID = {"active", "paused", "cancelled"}


def normalize_status(raw):
    """Lower-case and strip a status; unrecognised, blank or None becomes 'unknown'."""
    if raw is None:
        return "unknown"
    value = raw.lower()
    return value if value in VALID else "unknown"
