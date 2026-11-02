def net_price(gross, vat_rate):
    """Price excluding VAT, rounded to cents."""
    return round(gross / (1 + vat_rate), 2)
