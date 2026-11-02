import pandas as pd

from pricing.calc import net_price


def to_frame(items):
    """items: iterable of (sku, gross, vat_rate)."""
    rows = [(sku, gross, net_price(gross, rate)) for sku, gross, rate in items]
    return pd.DataFrame(rows, columns=["sku", "gross", "net"])
