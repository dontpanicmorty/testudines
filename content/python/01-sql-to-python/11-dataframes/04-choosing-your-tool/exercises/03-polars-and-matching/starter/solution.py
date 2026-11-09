import polars as pl


def top_polars(orders: list[dict], items: list[dict], n: int) -> list[tuple[int, float]]:
    """Top n customers by non-cancelled revenue using polars."""
    raise NotImplementedError


def normalise(rows) -> list[tuple[int, float]]:
    """Plain types, rounded, deterministic order."""
    raise NotImplementedError
