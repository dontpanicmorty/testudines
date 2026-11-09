import pandas as pd


def enrich_orders(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """LEFT JOIN customers onto orders and add full_name."""
    merged = orders.merge(
        customers[["customer_id", "first_name", "last_name"]],
        on="customer_id", how="left", validate="many_to_one",
    )
    merged = merged.assign(full_name=merged["first_name"] + " " + merged["last_name"])
    return merged[["order_id", "customer_id", "amount", "full_name"]]
