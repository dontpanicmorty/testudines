import pandas as pd


def paid_totals(orders: pd.DataFrame) -> pd.DataFrame:
    """Total paid amount per customer, biggest first."""
    paid = orders[orders["status"] == "paid"]
    out = paid.groupby("customer_id", as_index=False).agg(total=("amount", "sum"))
    return out.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
