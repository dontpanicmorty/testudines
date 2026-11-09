import sqlite3

import pytest

from solution import catalogue


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript("""
        CREATE TABLE author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
        CREATE TABLE book (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author_id INTEGER);
        INSERT INTO author (name) VALUES ('Aldo Marsh'), ('Wren Okafor');
    """)
    return c


def test_joined(conn):
    conn.executescript("""
        INSERT INTO book (title, author_id) VALUES ('Tide Tables', 1), ('Fen Atlas', 1), ('Reed Songs', 2);
    """)
    assert catalogue(conn) == [
        ("Fen Atlas", "Aldo Marsh"), ("Reed Songs", "Wren Okafor"), ("Tide Tables", "Aldo Marsh"),
    ]


def test_no_books(conn):
    assert catalogue(conn) == []


def test_book_without_author_is_left_out(conn):
    conn.execute("INSERT INTO book (title, author_id) VALUES ('Orphan', 99)")
    assert catalogue(conn) == []
