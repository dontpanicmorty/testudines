import sqlite3


def insert_events(conn: sqlite3.Connection, events: list[dict]) -> int:
    """Bulk insert, skipping existing event_ids. Return rows inserted."""
    if not events:
        return 0
    with conn:
        cur = conn.executemany(
            "INSERT OR IGNORE INTO events (event_id, user_id, kind) VALUES (:event_id, :user_id, :kind)",
            events,
        )
    return cur.rowcount
