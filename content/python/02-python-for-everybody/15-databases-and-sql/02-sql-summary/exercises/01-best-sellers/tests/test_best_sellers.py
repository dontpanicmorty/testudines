import sqlite3

import pytest

from solution import priciest


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE book (title TEXT, year INTEGER, price REAL)")
    c.executemany("INSERT INTO book VALUES (?, ?, ?)", [
        ("Tide Tables", 1999, 12.5), ("Moss and Stone", 2011, 8.0),
        ("Reed Songs", 2003, 15.0), ("Fen Atlas", 2010, 15.0),
    ])
    return c


def test_top_two(conn):
    assert priciest(conn, 2) == ["Fen Atlas", "Reed Songs"]


def test_more_than_exist(conn):
    assert priciest(conn, 10) == ["Fen Atlas", "Reed Songs", "Tide Tables", "Moss and Stone"]


def test_zero(conn):
    assert priciest(conn, 0) == []
