import sqlite3
from itertools import islice
from typing import Iterable


def load_rows(conn: sqlite3.Connection, rows: Iterable[tuple[int, str]], batch_size: int = 500) -> int:
    it = iter(rows)
    total = 0
    while batch := list(islice(it, batch_size)):
        conn.executemany("insert into events values (?, ?)", batch)
        conn.commit()
        total += len(batch)
    return total
