"""A blank string becomes 0.0 instead of None."""


def parse_amount(raw):
    """Parse '$1,234.50', '(12.00)' (negative), blank/'N/A'/None (None). Garbage raises ValueError."""
    if raw is None:
        return None
    text = raw.strip()
    if text == "":
        return 0.0
    if text.upper() == "N/A":
        return None
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()").replace("$", "").replace(",", "")
    value = float(text)
    return -value if negative else value
