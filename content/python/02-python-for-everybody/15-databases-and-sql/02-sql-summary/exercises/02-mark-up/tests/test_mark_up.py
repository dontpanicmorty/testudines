import sqlite3

import pytest

from solution import discount_old


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE book (title TEXT, year INTEGER, price REAL)")
    c.executemany("INSERT INTO book VALUES (?, ?, ?)", [
        ("A", 1990, 10.0), ("B", 2000, 20.0), ("C", 2010, 30.0),
    ])
    c.commit()
    return c


def prices(c):
    return dict(c.execute("SELECT title, price FROM book"))


def test_changes_only_older(conn):
    assert discount_old(conn, 2005, 50) == 2
    assert prices(conn) == {"A": 5.0, "B": 10.0, "C": 30.0}


def test_boundary_year_not_included(conn):
    assert discount_old(conn, 2000, 10) == 1
    assert prices(conn)["B"] == 20.0


def test_nothing_matches(conn):
    assert discount_old(conn, 1900, 10) == 0
    assert prices(conn) == {"A": 10.0, "B": 20.0, "C": 30.0}
