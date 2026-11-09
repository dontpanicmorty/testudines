import sqlite3

import pytest

from solution import clubs_of


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript("""
        CREATE TABLE member (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
        CREATE TABLE club (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
        CREATE TABLE membership (member_id INTEGER, club_id INTEGER, UNIQUE (member_id, club_id));
        INSERT INTO member (name) VALUES ('Ines'), ('Omar'), ('Kai');
        INSERT INTO club (name) VALUES ('Chess'), ('Birding'), ('Rowing');
        INSERT INTO membership VALUES (1, 1), (1, 2), (2, 2), (2, 3);
    """)
    return c


def test_two_clubs_sorted(conn):
    assert clubs_of(conn, "Ines") == ["Birding", "Chess"]


def test_other_member(conn):
    assert clubs_of(conn, "Omar") == ["Birding", "Rowing"]


def test_member_without_clubs(conn):
    assert clubs_of(conn, "Kai") == []


def test_unknown_member(conn):
    assert clubs_of(conn, "Nobody") == []
