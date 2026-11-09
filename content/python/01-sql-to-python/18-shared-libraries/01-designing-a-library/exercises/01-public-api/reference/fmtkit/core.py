def _normalize(name):
    return " ".join(name.split())


def clean_name(name):
    return _normalize(name).title()


def parse_amount(text):
    return float(text.strip().replace("$", "").replace(",", ""))
