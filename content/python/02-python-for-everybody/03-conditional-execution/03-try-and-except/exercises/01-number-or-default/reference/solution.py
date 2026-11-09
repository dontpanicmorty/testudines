def to_whole_number(text, fallback):
    try:
        return int(text)
    except ValueError:
        return fallback
