import sqlite3


def bikes_at(db_path, station):
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT bikes FROM reading WHERE station = ? ORDER BY rowid DESC LIMIT 1",
            (station,),
        ).fetchone()
    finally:
        conn.close()
    return None if row is None else row[0]
