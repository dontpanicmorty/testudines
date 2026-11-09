import polars as pl


def top_polars(orders: list[dict], items: list[dict], n: int) -> list[tuple[int, float]]:
    """Top n customers by non-cancelled revenue using polars."""
    if not orders or not items:
        return []
    out = (
        pl.DataFrame(orders).filter(pl.col("status") != "cancelled")
        .join(pl.DataFrame(items), on="order_id")
        .group_by("customer_id")
        .agg((pl.col("quantity") * pl.col("unit_price")).sum().round(2).alias("revenue"))
        .sort(["revenue", "customer_id"], descending=[True, False])
        .head(n)
    )
    return [(int(c), float(r)) for c, r in zip(out["customer_id"], out["revenue"])]


def normalise(rows) -> list[tuple[int, float]]:
    """Plain types, rounded, deterministic order."""
    cleaned = [(int(c), round(float(r), 2)) for c, r in rows]
    return sorted(cleaned, key=lambda t: (-t[1], t[0]))
