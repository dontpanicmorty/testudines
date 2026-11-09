import sqlite3

from solution import import_books


def test_ids_returned():
    conn = sqlite3.connect(":memory:")
    assert import_books(conn, [("Tide Tables", "Aldo"), ("Fen Atlas", "Aldo")]) == [1, 2]


def test_author_stored_once():
    conn = sqlite3.connect(":memory:")
    import_books(conn, [("A", "Aldo"), ("B", "Wren"), ("C", "Aldo")])
    assert conn.execute("SELECT COUNT(*) FROM author").fetchone()[0] == 2
    rows = conn.execute("SELECT title, author_id FROM book ORDER BY id").fetchall()
    assert rows == [("A", 1), ("B", 2), ("C", 1)]


def test_empty_creates_tables():
    conn = sqlite3.connect(":memory:")
    assert import_books(conn, []) == []
    assert conn.execute("SELECT COUNT(*) FROM book").fetchone()[0] == 0


def test_second_call_reuses_authors():
    conn = sqlite3.connect(":memory:")
    import_books(conn, [("A", "Aldo")])
    ids = import_books(conn, [("B", "Aldo")])
    assert ids == [2]
    assert conn.execute("SELECT COUNT(*) FROM author").fetchone()[0] == 1
