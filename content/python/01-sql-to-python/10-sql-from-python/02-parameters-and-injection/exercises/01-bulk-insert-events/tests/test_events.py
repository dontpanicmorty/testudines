import sqlite3
import pytest
from solution import insert_events


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE events (event_id TEXT PRIMARY KEY, user_id INTEGER, kind TEXT)")
    return c


def test_inserts_and_counts(conn):
    batch = [{"event_id": "e1", "user_id": 1, "kind": "login"},
             {"event_id": "e2", "user_id": 2, "kind": "it's odd'; DROP TABLE events;--"}]
    assert insert_events(conn, batch) == 2
    assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 2
    assert conn.execute("SELECT kind FROM events WHERE event_id='e2'").fetchone()[0].startswith("it's")


def test_rerun_is_noop(conn):
    batch = [{"event_id": "e1", "user_id": 1, "kind": "login"}]
    insert_events(conn, batch)
    assert insert_events(conn, batch) == 0
    assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 1


def test_partial_overlap_and_empty(conn):
    insert_events(conn, [{"event_id": "e1", "user_id": 1, "kind": "a"}])
    n = insert_events(conn, [{"event_id": "e1", "user_id": 1, "kind": "a"},
                             {"event_id": "e3", "user_id": 3, "kind": "c"}])
    assert n == 1
    assert insert_events(conn, []) == 0


def test_committed(conn):
    insert_events(conn, [{"event_id": "e1", "user_id": 1, "kind": "a"}])
    assert not conn.in_transaction, "load left an open transaction (not committed)"
