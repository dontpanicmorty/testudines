def parse_amount(text, *, currency="$"):
    return float(text.strip().replace(currency, "").replace(",", ""))
