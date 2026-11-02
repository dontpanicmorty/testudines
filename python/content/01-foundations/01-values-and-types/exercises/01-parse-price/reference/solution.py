def parse_price(text):
    return float(text.strip().replace("$", "").replace(",", ""))
