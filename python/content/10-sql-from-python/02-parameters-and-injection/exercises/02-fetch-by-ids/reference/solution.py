import sqlite3


def fetch_by_ids(conn: sqlite3.Connection, ids: list[int]) -> list[tuple]:
    ids = list(ids)
    if not ids:
        return []
    marks = ", ".join("?" * len(ids))
    sql = f"SELECT id, name FROM customers WHERE id IN ({marks}) ORDER BY id"
    return conn.execute(sql, ids).fetchall()
