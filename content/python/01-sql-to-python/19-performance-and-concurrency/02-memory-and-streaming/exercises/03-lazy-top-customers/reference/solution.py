import polars as pl


def top_customers(orders_csv, items_csv, n: int) -> pl.LazyFrame:
    orders = pl.scan_csv(orders_csv).filter(pl.col("status").is_in(["completed", "shipped"]))
    items = pl.scan_csv(items_csv)
    return (
        orders.join(items, on="order_id")
        .group_by("customer_id")
        .agg((pl.col("quantity") * pl.col("unit_price")).sum().round(2).alias("revenue"))
        .sort(["revenue", "customer_id"], descending=[True, False])
        .head(n)
    )
