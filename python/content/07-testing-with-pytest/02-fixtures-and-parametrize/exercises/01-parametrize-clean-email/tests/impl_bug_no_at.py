"""A value with no '@' is returned instead of None."""


def clean_email(raw):
    """Strip and lower-case; None for None, blank or invalid addresses."""
    if raw is None:
        return None
    value = raw.strip().lower()
    local, sep, domain = value.partition("@")
    if not sep:
        return value
    if not local or not domain or "@" in domain:
        return None
    return value
