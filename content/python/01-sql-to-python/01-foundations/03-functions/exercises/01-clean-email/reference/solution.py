def clean_email(email):
    """Return a trimmed, lowercased email, or None if blank."""
    if email is None:
        return None
    return email.strip().lower() or None
