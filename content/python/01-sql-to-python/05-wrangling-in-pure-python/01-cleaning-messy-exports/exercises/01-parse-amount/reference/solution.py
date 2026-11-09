from decimal import Decimal, InvalidOperation


def parse_amount(text):
    text = (text or "").strip()
    if text == "" or text.lower() == "n/a":
        return None
    cleaned = text.replace("$", "").replace(",", "").strip()
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        raise ValueError(f"bad amount: {text!r}") from None
