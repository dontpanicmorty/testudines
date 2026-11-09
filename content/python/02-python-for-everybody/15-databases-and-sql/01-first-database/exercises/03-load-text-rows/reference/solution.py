import sqlite3


def load_feed(db_path, text):
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS reading (station TEXT, bikes INTEGER)")
    inserted = 0
    skipped = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 2:
            skipped += 1
            continue
        try:
            bikes = int(parts[1])
        except ValueError:
            skipped += 1
            continue
        conn.execute("INSERT INTO reading (station, bikes) VALUES (?, ?)", (parts[0].strip(), bikes))
        inserted += 1
    conn.commit()
    conn.close()
    return (inserted, skipped)
