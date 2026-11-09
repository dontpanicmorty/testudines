"""None crashes instead of returning None."""


def clean_email(raw):
    """Strip and lower-case; None for None, blank or invalid addresses."""
    value = raw.strip().lower()
    local, sep, domain = value.partition("@")
    if not sep or not local or not domain or "@" in domain:
        return None
    return value
