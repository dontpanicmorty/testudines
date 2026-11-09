def parse_age(text):
    try:
        age = int(text)
    except ValueError:
        return None
    if 0 <= age <= 120:
        return age
    return None
