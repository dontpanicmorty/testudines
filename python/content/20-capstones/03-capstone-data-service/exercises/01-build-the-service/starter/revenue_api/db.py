"""DuckDB access: a connection per request."""
from typing import Any, Iterator, Sequence

import duckdb

from .settings import Settings


def connect(db_path: str) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(db_path)


def get_conn(settings: Settings) -> Iterator[duckdb.DuckDBPyConnection]:
    """FastAPI dependency: open a connection for the request and always close it afterwards.

    TODO: it needs the current settings, injected through the settings dependency.
    """
    raise NotImplementedError


def fetch_all(conn: duckdb.DuckDBPyConnection, sql: str, params: Sequence[Any] = ()) -> list[dict]:
    """Run a query and return rows as dicts keyed by column name."""
    raise NotImplementedError
