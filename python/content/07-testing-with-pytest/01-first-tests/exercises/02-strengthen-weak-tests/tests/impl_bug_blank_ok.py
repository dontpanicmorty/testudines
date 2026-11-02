"""A blank string is returned as blank instead of 'unknown'."""

VALID = {"active", "paused", "cancelled"}


def normalize_status(raw):
    """Lower-case and strip a status; unrecognised, blank or None becomes 'unknown'."""
    if raw is None:
        return "unknown"
    value = raw.strip().lower()
    return value if value in VALID or value == "" else "unknown"
