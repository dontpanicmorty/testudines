"""DuckDB access: a connection per request."""
from typing import Any, Iterator, Sequence

import duckdb
from fastapi import Depends

from .settings import Settings, get_settings


def connect(db_path: str) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(db_path)


def get_conn(settings: Settings = Depends(get_settings)) -> Iterator[duckdb.DuckDBPyConnection]:
    conn = connect(settings.db_path)
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(conn: duckdb.DuckDBPyConnection, sql: str, params: Sequence[Any] = ()) -> list[dict]:
    cursor = conn.execute(sql, list(params))
    names = [d[0] for d in cursor.description]
    return [dict(zip(names, row)) for row in cursor.fetchall()]
