import sqlite3
import pytest
from solution import transfer


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE acct (id INTEGER PRIMARY KEY, balance INTEGER)")
    c.execute("INSERT INTO acct VALUES (1, 100), (2, 50)")
    c.commit()
    return c


def balances(c):
    return c.execute("SELECT id, balance FROM acct ORDER BY id").fetchall()


def test_happy_path(conn):
    transfer(conn, 1, 2, 30)
    assert balances(conn) == [(1, 70), (2, 80)]


def test_unknown_destination_rolls_back(conn):
    with pytest.raises(ValueError):
        transfer(conn, 1, 99, 30)
    conn.rollback()
    assert balances(conn) == [(1, 100), (2, 50)], "source balance changed even though the transfer failed"


def test_unknown_source(conn):
    with pytest.raises(ValueError):
        transfer(conn, 99, 2, 30)
    conn.rollback()
    assert balances(conn) == [(1, 100), (2, 50)]


def test_insufficient_funds_rolls_back(conn):
    with pytest.raises(ValueError):
        transfer(conn, 1, 2, 10_000)
    conn.rollback()
    assert balances(conn) == [(1, 100), (2, 50)], "an overdraft was committed"
