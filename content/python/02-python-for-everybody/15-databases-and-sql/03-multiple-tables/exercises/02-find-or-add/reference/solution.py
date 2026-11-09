def author_id(conn, name):
    conn.execute("INSERT OR IGNORE INTO author (name) VALUES (?)", (name,))
    row = conn.execute("SELECT id FROM author WHERE name = ?", (name,)).fetchone()
    conn.commit()
    return row[0]
