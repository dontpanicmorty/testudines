"""Amounts in parentheses come out positive instead of negative."""


def parse_amount(raw):
    """Parse '$1,234.50', '(12.00)' (negative), blank/'N/A'/None (None). Garbage raises ValueError."""
    if raw is None:
        return None
    text = raw.strip()
    if text == "" or text.upper() == "N/A":
        return None
    negative = False
    text = text.strip("()").replace("$", "").replace(",", "")
    value = float(text)
    return -value if negative else value
