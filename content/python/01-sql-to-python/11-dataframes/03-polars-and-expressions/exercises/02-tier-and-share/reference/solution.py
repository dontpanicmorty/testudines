import polars as pl


def add_tier_and_share(df: pl.DataFrame) -> pl.DataFrame:
    """Add tier (CASE WHEN) and region_share (window)."""
    return df.with_columns(
        pl.when(pl.col("amount") >= 100).then(pl.lit("large"))
        .when(pl.col("amount") >= 50).then(pl.lit("medium"))
        .otherwise(pl.lit("small"))
        .alias("tier"),
        (pl.col("amount") / pl.col("amount").sum().over("region")).round(3).alias("region_share"),
    )
