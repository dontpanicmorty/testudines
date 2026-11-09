import duckdb


def running_totals(entries: list[tuple[str, str, int]]) -> list[tuple[str, str, int, int]]:
    """Cumulative amount per account, in date order, via a window function."""
    raise NotImplementedError
