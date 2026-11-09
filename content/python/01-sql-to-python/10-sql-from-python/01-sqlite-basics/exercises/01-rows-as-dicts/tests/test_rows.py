import sqlite3
from solution import query_dicts


def make():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE t (id INTEGER, name TEXT)")
    conn.executemany("INSERT INTO t VALUES (?, ?)", [(1, "Ada"), (2, "Linus")])
    return conn


def test_rows_are_dicts():
    out = query_dicts(make(), "SELECT id, name FROM t ORDER BY id")
    assert out == [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Linus"}], out


def test_empty_result():
    assert query_dicts(make(), "SELECT * FROM t WHERE id > 99") == []


def test_row_factory_restored():
    conn = make()
    query_dicts(conn, "SELECT * FROM t")
    assert conn.row_factory is None, "row_factory should be restored to what it was"
    assert conn.execute("SELECT id FROM t ORDER BY id").fetchone() == (1,)
