import pandas as pd


def top_pandas(orders: list[dict], items: list[dict], n: int) -> list[tuple[int, float]]:
    """Top n customers by non-cancelled revenue using pandas."""
    if not orders or not items:
        return []
    o = pd.DataFrame(orders)
    o = o[o["status"] != "cancelled"]
    df = o.merge(pd.DataFrame(items), on="order_id")
    df = df.assign(revenue=df["quantity"] * df["unit_price"])
    totals = df.groupby("customer_id", as_index=False)["revenue"].sum()
    totals = totals.assign(revenue=totals["revenue"].round(2))
    totals = totals.sort_values(["revenue", "customer_id"], ascending=[False, True]).head(n)
    return [(int(c), float(r)) for c, r in zip(totals["customer_id"], totals["revenue"])]
