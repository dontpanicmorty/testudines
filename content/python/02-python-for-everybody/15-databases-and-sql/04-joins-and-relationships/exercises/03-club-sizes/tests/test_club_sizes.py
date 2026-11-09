import sqlite3

import pytest

from solution import club_sizes


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript("""
        CREATE TABLE club (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
        CREATE TABLE membership (member_id INTEGER, club_id INTEGER, UNIQUE (member_id, club_id));
        INSERT INTO club (name) VALUES ('Chess'), ('Birding'), ('Rowing'), ('Quilting');
    """)
    return c


def test_counts_and_order(conn):
    conn.executescript("INSERT INTO membership VALUES (1, 1), (2, 1), (3, 1), (1, 2), (2, 3);")
    assert club_sizes(conn) == [("Chess", 3), ("Birding", 1), ("Rowing", 1), ("Quilting", 0)]


def test_all_empty_sorted_by_name(conn):
    assert club_sizes(conn) == [("Birding", 0), ("Chess", 0), ("Quilting", 0), ("Rowing", 0)]


def test_no_clubs():
    c = sqlite3.connect(":memory:")
    c.executescript("""
        CREATE TABLE club (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
        CREATE TABLE membership (member_id INTEGER, club_id INTEGER);
    """)
    assert club_sizes(c) == []
