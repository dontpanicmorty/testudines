import sqlite3


def query_dicts(conn: sqlite3.Connection, sql: str) -> list[dict]:
    """Run a SELECT and return a list of dicts. Restore conn.row_factory afterwards."""
    previous = conn.row_factory
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(sql)]
    finally:
        conn.row_factory = previous
