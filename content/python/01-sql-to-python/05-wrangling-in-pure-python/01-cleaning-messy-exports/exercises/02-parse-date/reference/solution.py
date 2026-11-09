from datetime import date, datetime

FORMATS = ("%Y-%m-%d", "%d %b %Y", "%m/%d/%Y")


def parse_date(text):
    cleaned = text.strip()
    for fmt in FORMATS:
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unrecognised date: {text!r}")
