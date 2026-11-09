from pricing.calc import net_price


def to_frame(items):
    """items: iterable of (sku, gross, vat_rate)."""
    import pandas as pd

    rows = [(sku, gross, net_price(gross, rate)) for sku, gross, rate in items]
    return pd.DataFrame(rows, columns=["sku", "gross", "net"])
