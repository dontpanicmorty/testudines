import sqlite3


def upsert_customers(conn: sqlite3.Connection, rows: list[dict]) -> None:
    with conn:
        conn.executemany(
            "INSERT OR REPLACE INTO customers (id, email, updated_at) "
            "VALUES (:id, :email, :updated_at)",
            rows,
        )
