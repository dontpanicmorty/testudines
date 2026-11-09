import sqlite3


def retire(db_path, cutoff_year, max_price):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("DELETE FROM book WHERE year < ? AND price < ?", (cutoff_year, max_price))
        removed = cur.rowcount
        conn.commit()
        remaining = conn.execute("SELECT COUNT(*) FROM book").fetchone()[0]
    finally:
        conn.close()
    return (removed, remaining)
