import duckdb
import pytest

from solution import latest_per_key


@pytest.fixture()
def con():
    c = duckdb.connect(":memory:")
    c.execute("CREATE TABLE customers (id INTEGER, email TEXT, updated_at INTEGER)")
    c.execute("""INSERT INTO customers VALUES
        (2, 'only@x.test', 5),
        (1, 'old@x.test', 1),
        (1, 'new@x.test', 3),
        (1, 'mid@x.test', 2),
        (3, 'c-old@x.test', 9),
        (3, 'c-new@x.test', 10)""")
    return c


def test_latest_row_per_key_ordered(con):
    assert latest_per_key(con, "customers", "id", "updated_at") == [
        {"id": 1, "email": "new@x.test", "updated_at": 3},
        {"id": 2, "email": "only@x.test", "updated_at": 5},
        {"id": 3, "email": "c-new@x.test", "updated_at": 10},
    ]


def test_ties_return_single_row(con):
    con.execute("INSERT INTO customers VALUES (2, 'dup@x.test', 5)")
    got = latest_per_key(con, "customers", "id", "updated_at")
    assert [r["id"] for r in got] == [1, 2, 3]


def test_empty_table():
    c = duckdb.connect(":memory:")
    c.execute("CREATE TABLE t (k INTEGER, ts INTEGER)")
    assert latest_per_key(c, "t", "k", "ts") == []


def test_other_column_names():
    c = duckdb.connect(":memory:")
    c.execute("CREATE TABLE ev (user_id TEXT, seen TEXT, v INTEGER)")
    c.execute("INSERT INTO ev VALUES ('a', '2026-01-01', 1), ('a', '2026-02-01', 2)")
    assert latest_per_key(c, "ev", "user_id", "seen") == [{"user_id": "a", "seen": "2026-02-01", "v": 2}]


def test_rejects_unsafe_identifiers(con):
    for args in [("customers; DROP TABLE customers", "id", "updated_at"),
                 ("customers", "id) --", "updated_at"),
                 ("customers", "id", "")]:
        with pytest.raises(ValueError):
            latest_per_key(con, *args)
