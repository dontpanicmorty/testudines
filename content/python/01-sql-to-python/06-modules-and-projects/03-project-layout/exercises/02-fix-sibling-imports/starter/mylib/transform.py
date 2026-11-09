from cleaning import clean_email, clean_name


def normalize_rows(rows):
    return [
        {"name": clean_name(r["name"]), "email": clean_email(r["email"])} for r in rows
    ]
