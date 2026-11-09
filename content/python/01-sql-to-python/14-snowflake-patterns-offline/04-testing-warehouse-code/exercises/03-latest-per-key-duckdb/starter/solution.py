"""Logic you can verify on an in-memory DuckDB."""


def latest_per_key(con, table: str, key: str, ts_col: str) -> list[dict]:
    ...
