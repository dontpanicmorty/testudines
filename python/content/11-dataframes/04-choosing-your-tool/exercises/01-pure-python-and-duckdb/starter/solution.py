import duckdb


def top_python(orders: list[dict], items: list[dict], n: int) -> list[tuple[int, float]]:
    """Plain Python: dicts and loops."""
    raise NotImplementedError


def top_duckdb(orders: list[dict], items: list[dict], n: int) -> list[tuple[int, float]]:
    """DuckDB: load the rows into in-memory tables and run one query."""
    raise NotImplementedError
