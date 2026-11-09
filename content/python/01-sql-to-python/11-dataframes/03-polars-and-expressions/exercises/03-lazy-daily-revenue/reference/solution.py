import polars as pl


def daily_revenue(orders_path, items_path) -> pl.DataFrame:
    """Lazy scan, join, filter, group by day. See prompt.md."""
    orders = pl.scan_csv(orders_path).filter(pl.col("status") != "cancelled")
    items = pl.scan_csv(items_path)
    return (
        orders.join(items, on="order_id", how="inner")
        .with_columns(pl.col("placed_at").cast(pl.String).str.slice(0, 10).alias("day"))
        .group_by("day")
        .agg((pl.col("quantity") * pl.col("unit_price")).sum().round(2).alias("revenue"))
        .sort("day")
        .collect()
    )
