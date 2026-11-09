"""Garbage input returns None instead of raising ValueError."""


def parse_amount(raw):
    """Parse '$1,234.50', '(12.00)' (negative), blank/'N/A'/None (None). Garbage raises ValueError."""
    if raw is None:
        return None
    text = raw.strip()
    if text == "" or text.upper() == "N/A":
        return None
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()").replace("$", "").replace(",", "")
    try:
        value = float(text)
    except ValueError:
        return None
    return -value if negative else value
