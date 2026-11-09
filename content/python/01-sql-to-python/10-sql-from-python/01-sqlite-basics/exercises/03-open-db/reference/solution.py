import sqlite3


def open_db(path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    with conn:
        conn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, started TEXT NOT NULL)")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS run_rows ("
            "id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL REFERENCES runs(id), payload TEXT)"
        )
    return conn
