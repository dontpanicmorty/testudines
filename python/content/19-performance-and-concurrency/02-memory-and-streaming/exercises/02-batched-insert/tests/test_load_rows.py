import sqlite3

from solution import load_rows


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute("create table events(id integer, kind text)")
    return conn


def count(conn):
    return conn.execute("select count(*) from events").fetchone()[0]


def test_inserts_all_and_returns_count():
    conn = make_conn()
    assert load_rows(conn, [(i, "click") for i in range(10)], batch_size=4) == 10
    assert count(conn) == 10


def test_empty_input():
    conn = make_conn()
    assert load_rows(conn, [], batch_size=4) == 0
    assert count(conn) == 0


def test_accepts_generator():
    conn = make_conn()
    assert load_rows(conn, ((i, "x") for i in range(7)), batch_size=3) == 7


def test_exact_multiple_of_batch():
    conn = make_conn()
    assert load_rows(conn, [(i, "x") for i in range(8)], batch_size=4) == 8


def test_never_holds_more_than_one_batch():
    conn = make_conn()
    lags = []

    def producer(n):
        for i in range(n):
            lags.append(i - count(conn))     # rows produced but not yet written
            yield (i, "click")

    assert load_rows(conn, producer(1000), batch_size=50) == 1000
    assert max(lags) <= 50, f"{max(lags)} rows were buffered at once; the limit is the batch size"


def test_writes_happen_before_input_is_exhausted():
    conn = make_conn()
    seen = {}

    def producer():
        for i in range(100):
            if i == 90:
                seen["written_so_far"] = count(conn)
            yield (i, "x")

    load_rows(conn, producer(), batch_size=10)
    assert seen["written_so_far"] >= 80
