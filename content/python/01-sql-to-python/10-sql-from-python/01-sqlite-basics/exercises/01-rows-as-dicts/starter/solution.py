import sqlite3


def query_dicts(conn: sqlite3.Connection, sql: str) -> list[dict]:
    """Run a SELECT and return a list of dicts. Restore conn.row_factory afterwards."""
    raise NotImplementedError
