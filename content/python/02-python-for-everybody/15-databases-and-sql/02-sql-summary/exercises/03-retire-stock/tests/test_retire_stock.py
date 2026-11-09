import sqlite3

import pytest

from solution import retire


@pytest.fixture
def db(tmp_path):
    path = str(tmp_path / "shop.db")
    c = sqlite3.connect(path)
    c.execute("CREATE TABLE book (title TEXT, year INTEGER, price REAL)")
    c.executemany("INSERT INTO book VALUES (?, ?, ?)", [
        ("old cheap", 1990, 3.0), ("old dear", 1991, 30.0),
        ("new cheap", 2015, 2.0), ("old cheap 2", 1985, 4.5),
    ])
    c.commit()
    c.close()
    return path


def titles(path):
    c = sqlite3.connect(path)
    try:
        return sorted(r[0] for r in c.execute("SELECT title FROM book"))
    finally:
        c.close()


def test_both_conditions(db):
    assert retire(db, 2000, 5.0) == (2, 2)
    assert titles(db) == ["new cheap", "old dear"]


def test_nothing_removed(db):
    assert retire(db, 1900, 1.0) == (0, 4)


def test_everything_removed(db):
    assert retire(db, 3000, 1000.0) == (4, 0)
    assert titles(db) == []
