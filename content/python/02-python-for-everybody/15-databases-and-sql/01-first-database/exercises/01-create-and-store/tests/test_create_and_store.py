import sqlite3

from solution import store_readings


def stored(path):
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT station, bikes FROM reading ORDER BY rowid").fetchall()
    finally:
        conn.close()


def test_saved_to_disk(tmp_path):
    db = str(tmp_path / "b.db")
    assert store_readings(db, [("Mill Lane", 4), ("Hill Top", 9)]) == 2
    assert stored(db) == [("Mill Lane", 4), ("Hill Top", 9)]


def test_appends_second_call(tmp_path):
    db = str(tmp_path / "b.db")
    store_readings(db, [("A", 1)])
    store_readings(db, [("B", 2)])
    assert stored(db) == [("A", 1), ("B", 2)]


def test_empty_list(tmp_path):
    db = str(tmp_path / "b.db")
    assert store_readings(db, []) == 0
    assert stored(db) == []


def test_apostrophe_name(tmp_path):
    db = str(tmp_path / "b.db")
    store_readings(db, [("O'Neil Quay", 3)])
    assert stored(db) == [("O'Neil Quay", 3)]
