import sqlite3


def insert_events(conn: sqlite3.Connection, events: list[dict]) -> int:
    """Bulk insert, skipping existing event_ids. Return rows inserted."""
    raise NotImplementedError
