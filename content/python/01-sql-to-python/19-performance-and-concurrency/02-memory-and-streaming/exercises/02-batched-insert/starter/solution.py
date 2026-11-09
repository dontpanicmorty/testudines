import sqlite3
from typing import Iterable


def load_rows(conn: sqlite3.Connection, rows: Iterable[tuple[int, str]], batch_size: int = 500) -> int:
    rows = list(rows)
    for start in range(0, len(rows), batch_size):
        conn.executemany("insert into events values (?, ?)", rows[start:start + batch_size])
    conn.commit()
    return len(rows)
