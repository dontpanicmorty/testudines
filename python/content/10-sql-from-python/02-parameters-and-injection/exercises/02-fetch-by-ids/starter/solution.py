import sqlite3


def fetch_by_ids(conn: sqlite3.Connection, ids: list[int]) -> list[tuple]:
    sql = f"SELECT id, name FROM customers WHERE id IN {tuple(ids)} ORDER BY id"
    return conn.execute(sql).fetchall()
