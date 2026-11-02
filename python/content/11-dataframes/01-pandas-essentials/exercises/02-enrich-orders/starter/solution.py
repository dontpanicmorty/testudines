import pandas as pd


def enrich_orders(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """LEFT JOIN customers onto orders and add full_name."""
    raise NotImplementedError
