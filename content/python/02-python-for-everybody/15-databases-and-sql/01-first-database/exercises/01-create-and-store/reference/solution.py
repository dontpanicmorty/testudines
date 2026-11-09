import sqlite3


def store_readings(db_path, rows):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS reading (station TEXT, bikes INTEGER)")
    cur.executemany("INSERT INTO reading (station, bikes) VALUES (?, ?)", rows)
    conn.commit()
    conn.close()
    return len(rows)
