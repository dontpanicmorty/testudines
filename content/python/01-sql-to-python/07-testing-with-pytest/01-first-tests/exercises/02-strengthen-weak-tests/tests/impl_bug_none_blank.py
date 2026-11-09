"""None becomes an empty string instead of 'unknown'."""

VALID = {"active", "paused", "cancelled"}


def normalize_status(raw):
    """Lower-case and strip a status; unrecognised, blank or None becomes 'unknown'."""
    if raw is None:
        return ""
    value = raw.strip().lower()
    return value if value in VALID else "unknown"
