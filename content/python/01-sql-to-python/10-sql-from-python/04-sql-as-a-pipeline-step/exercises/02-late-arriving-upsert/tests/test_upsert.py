import sqlite3
import pytest
from solution import upsert_customers


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, email TEXT, updated_at TEXT)")
    return c


def state(c):
    return c.execute("SELECT id, email, updated_at FROM customers ORDER BY id").fetchall()


def test_insert_and_update(conn):
    upsert_customers(conn, [{"id": 1, "email": "a@x", "updated_at": "2025-01-01"}])
    upsert_customers(conn, [{"id": 1, "email": "b@x", "updated_at": "2025-01-05"},
                            {"id": 2, "email": "c@x", "updated_at": "2025-01-02"}])
    assert state(conn) == [(1, "b@x", "2025-01-05"), (2, "c@x", "2025-01-02")]


def test_replay_is_noop(conn):
    batch = [{"id": 1, "email": "a@x", "updated_at": "2025-01-01"}]
    upsert_customers(conn, batch)
    upsert_customers(conn, batch)
    assert state(conn) == [(1, "a@x", "2025-01-01")]


def test_late_older_record_ignored(conn):
    upsert_customers(conn, [{"id": 1, "email": "new@x", "updated_at": "2025-03-01"}])
    upsert_customers(conn, [{"id": 1, "email": "old@x", "updated_at": "2025-01-01"}])
    assert state(conn) == [(1, "new@x", "2025-03-01")], "an older record overwrote a newer one"


def test_same_batch_order_does_not_matter(conn):
    batch = [{"id": 1, "email": "new@x", "updated_at": "2025-03-01"},
             {"id": 1, "email": "old@x", "updated_at": "2025-01-01"}]
    upsert_customers(conn, batch)
    assert state(conn) == [(1, "new@x", "2025-03-01")]
