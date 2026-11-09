import sqlite3
import pytest
from solution import fetch_by_ids


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE customers (id INTEGER, name TEXT)")
    c.executemany("INSERT INTO customers VALUES (?, ?)", [(1, "Ada"), (2, "Linus"), (3, "Tim")])
    return c


def test_many(conn):
    assert fetch_by_ids(conn, [3, 1]) == [(1, "Ada"), (3, "Tim")]


def test_single(conn):
    assert fetch_by_ids(conn, [3]) == [(3, "Tim")]


def test_empty(conn):
    assert fetch_by_ids(conn, []) == []


def test_missing_ids_ignored(conn):
    assert fetch_by_ids(conn, [2, 99]) == [(2, "Linus")]


def test_accepts_tuple_and_generator(conn):
    assert fetch_by_ids(conn, (1, 2)) == [(1, "Ada"), (2, "Linus")]
    assert fetch_by_ids(conn, (i for i in [2])) == [(2, "Linus")]


def test_no_sql_text_from_data(conn):
    # a non-int id must be treated as a value, never executed
    assert fetch_by_ids(conn, ["1 OR 1=1"]) == []
