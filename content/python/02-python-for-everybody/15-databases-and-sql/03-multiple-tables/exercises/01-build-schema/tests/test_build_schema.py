import sqlite3

import pytest

from solution import create_schema


def columns(conn, table):
    return [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]


def test_tables_exist():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    assert columns(conn, "author") == ["id", "name"]
    assert columns(conn, "book") == ["id", "title", "author_id"]


def test_ids_assigned_automatically():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    c1 = conn.execute("INSERT INTO author (name) VALUES ('A')")
    c2 = conn.execute("INSERT INTO author (name) VALUES ('B')")
    assert (c1.lastrowid, c2.lastrowid) == (1, 2)


def test_duplicate_name_rejected():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    conn.execute("INSERT INTO author (name) VALUES ('A')")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO author (name) VALUES ('A')")


def test_safe_to_call_twice():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    conn.execute("INSERT INTO author (name) VALUES ('A')")
    create_schema(conn)
    assert conn.execute("SELECT COUNT(*) FROM author").fetchone()[0] == 1
