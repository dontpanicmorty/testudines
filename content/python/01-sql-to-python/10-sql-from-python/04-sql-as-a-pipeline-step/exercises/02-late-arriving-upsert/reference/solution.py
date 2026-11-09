import sqlite3

UPSERT = """
INSERT INTO customers (id, email, updated_at) VALUES (:id, :email, :updated_at)
ON CONFLICT (id) DO UPDATE SET
    email = excluded.email,
    updated_at = excluded.updated_at
WHERE excluded.updated_at > customers.updated_at
"""


def upsert_customers(conn: sqlite3.Connection, rows: list[dict]) -> None:
    with conn:
        conn.executemany(UPSERT, rows)
