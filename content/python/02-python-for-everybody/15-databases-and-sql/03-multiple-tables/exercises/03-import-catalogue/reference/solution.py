def import_books(conn, pairs):
    conn.execute("CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author_id INTEGER)"
    )
    ids = []
    for title, name in pairs:
        conn.execute("INSERT OR IGNORE INTO author (name) VALUES (?)", (name,))
        aid = conn.execute("SELECT id FROM author WHERE name = ?", (name,)).fetchone()[0]
        cur = conn.execute("INSERT INTO book (title, author_id) VALUES (?, ?)", (title, aid))
        ids.append(cur.lastrowid)
    conn.commit()
    return ids
