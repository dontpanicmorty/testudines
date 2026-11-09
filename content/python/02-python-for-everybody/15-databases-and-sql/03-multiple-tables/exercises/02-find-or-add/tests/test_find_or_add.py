import sqlite3

import pytest

from solution import author_id


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
    return c


def test_new_names_get_new_ids(conn):
    assert author_id(conn, "Aldo") == 1
    assert author_id(conn, "Wren") == 2


def test_same_name_same_id(conn):
    first = author_id(conn, "Aldo")
    author_id(conn, "Wren")
    assert author_id(conn, "Aldo") == first


def test_no_duplicate_rows(conn):
    for _ in range(3):
        author_id(conn, "Aldo")
    assert conn.execute("SELECT COUNT(*) FROM author").fetchone()[0] == 1


def test_existing_row_is_found(conn):
    conn.execute("INSERT INTO author (name) VALUES ('Pre')")
    conn.execute("INSERT INTO author (name) VALUES ('Existing')")
    assert author_id(conn, "Existing") == 2
