"""None crashes with AttributeError instead of returning None."""


def parse_amount(raw):
    """Parse '$1,234.50', '(12.00)' (negative), blank/'N/A'/None (None). Garbage raises ValueError."""
    text = raw.strip()
    if text == "" or text.upper() == "N/A":
        return None
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()").replace("$", "").replace(",", "")
    value = float(text)
    return -value if negative else value
