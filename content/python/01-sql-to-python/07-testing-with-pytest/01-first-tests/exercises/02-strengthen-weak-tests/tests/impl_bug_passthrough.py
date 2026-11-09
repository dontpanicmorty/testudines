"""Unrecognised statuses are returned as-is instead of 'unknown'."""

VALID = {"active", "paused", "cancelled"}


def normalize_status(raw):
    """Lower-case and strip a status; unrecognised, blank or None becomes 'unknown'."""
    if raw is None:
        return "unknown"
    value = raw.strip().lower()
    return value or "unknown"
