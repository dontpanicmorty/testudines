import polars as pl


def region_revenue(orders: pl.DataFrame) -> pl.DataFrame:
    """Orders and revenue per region, excluding cancelled."""
    return (
        orders.filter(pl.col("status") != "cancelled")
        .group_by("region")
        .agg(pl.len().alias("n_orders"), pl.col("amount").sum().alias("total"))
        .sort(["total", "region"], descending=[True, False])
    )
