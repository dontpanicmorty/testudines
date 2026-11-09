import sqlite3

import pytest

from solution import load_partition


def make_conn():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "create table fact_orders (load_date text, order_id int not null, amount real)"
    )
    return conn


def count(conn, d=None):
    if d is None:
        return conn.execute("select count(*) from fact_orders").fetchone()[0]
    return conn.execute(
        "select count(*) from fact_orders where load_date = ?", (d,)
    ).fetchone()[0]


def test_rerun_is_idempotent():
    conn = make_conn()
    rows = [(1, 10.0), (2, 5.0)]
    load_partition(conn, "2026-01-01", rows)
    load_partition(conn, "2026-01-01", rows)
    assert count(conn, "2026-01-01") == 2


def test_other_dates_untouched():
    conn = make_conn()
    load_partition(conn, "2026-01-01", [(1, 1.0)])
    load_partition(conn, "2026-01-02", [(2, 2.0), (3, 3.0)])
    load_partition(conn, "2026-01-02", [(2, 2.0), (3, 3.0)])
    assert count(conn, "2026-01-01") == 1
    assert count(conn, "2026-01-02") == 2


def test_rerun_replaces_content():
    conn = make_conn()
    load_partition(conn, "2026-01-01", [(1, 1.0), (2, 2.0)])
    load_partition(conn, "2026-01-01", [(9, 9.0)])
    assert conn.execute("select order_id from fact_orders").fetchall() == [(9,)]


def test_failed_reload_keeps_old_data():
    conn = make_conn()
    load_partition(conn, "2026-01-01", [(1, 1.0), (2, 2.0)])
    with pytest.raises(sqlite3.IntegrityError):
        load_partition(conn, "2026-01-01", [(5, 5.0), (None, 6.0)])
    assert count(conn, "2026-01-01") == 2
    assert sorted(r[0] for r in conn.execute("select order_id from fact_orders")) == [1, 2]
