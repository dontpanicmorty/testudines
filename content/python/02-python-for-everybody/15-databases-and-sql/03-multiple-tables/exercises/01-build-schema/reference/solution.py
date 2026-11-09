def create_schema(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author_id INTEGER)"
    )
    conn.commit()
