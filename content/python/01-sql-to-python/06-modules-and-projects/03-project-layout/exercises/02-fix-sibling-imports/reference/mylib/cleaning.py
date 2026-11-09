def clean_name(raw):
    return " ".join(raw.split()).title()


def clean_email(raw):
    return raw.strip().lower()
