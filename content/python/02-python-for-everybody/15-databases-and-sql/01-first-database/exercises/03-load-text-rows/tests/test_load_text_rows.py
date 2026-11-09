import sqlite3

from solution import load_feed


def rows(path):
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT station, bikes FROM reading ORDER BY rowid").fetchall()
    finally:
        conn.close()


def test_mixed(tmp_path):
    db = str(tmp_path / "b.db")
    assert load_feed(db, "Mill Lane,4\nbad line\nHill Top,nine\n") == (1, 2)
    assert rows(db) == [("Mill Lane", 4)]


def test_all_good(tmp_path):
    db = str(tmp_path / "b.db")
    assert load_feed(db, "A,1\nB,2") == (2, 0)
    assert rows(db) == [("A", 1), ("B", 2)]


def test_blank_lines_ignored(tmp_path):
    db = str(tmp_path / "b.db")
    assert load_feed(db, "\n\nA,1\n   \n") == (1, 0)


def test_empty_text_still_creates_table(tmp_path):
    db = str(tmp_path / "b.db")
    assert load_feed(db, "") == (0, 0)
    assert rows(db) == []


def test_too_many_commas(tmp_path):
    db = str(tmp_path / "b.db")
    assert load_feed(db, "A,1,2\nB,3") == (1, 1)
    assert rows(db) == [("B", 3)]
