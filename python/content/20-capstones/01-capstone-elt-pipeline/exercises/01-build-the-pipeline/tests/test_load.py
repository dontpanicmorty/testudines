import sqlite3

from pipeline import load


def rows(day, region="west", orders=1, revenue=10.0):
    return {"day": day, "region": region, "orders": orders, "revenue": revenue}


def all_rows(conn):
    return conn.execute("select day, region, orders, revenue from daily_revenue order by 1, 2").fetchall()


def test_connect_creates_tables(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    names = {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}
    assert {"daily_revenue", "quarantine", "pipeline_state"} <= names
    conn.close()


def test_connect_twice_is_fine(tmp_path):
    load.connect(tmp_path / "x.db").close()
    load.connect(tmp_path / "x.db").close()


def test_load_returns_count_and_inserts(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    assert load.load_daily_revenue(conn, [rows("2025-01-01"), rows("2025-01-02")]) == 2
    assert all_rows(conn) == [("2025-01-01", "west", 1, 10.0), ("2025-01-02", "west", 1, 10.0)]


def test_load_twice_is_idempotent(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    data = [rows("2025-01-01"), rows("2025-01-01", "east")]
    load.load_daily_revenue(conn, data)
    load.load_daily_revenue(conn, data)
    assert len(all_rows(conn)) == 2


def test_partition_replace_changes_only_given_days(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    load.load_daily_revenue(conn, [rows("2025-01-01", revenue=1.0), rows("2025-01-02", revenue=2.0)])
    load.load_daily_revenue(conn, [rows("2025-01-02", revenue=99.0)])
    assert all_rows(conn) == [("2025-01-01", "west", 1, 1.0), ("2025-01-02", "west", 1, 99.0)]


def test_partition_replace_removes_stale_region_in_reloaded_day(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    load.load_daily_revenue(conn, [rows("2025-01-01", "west"), rows("2025-01-01", "east")])
    load.load_daily_revenue(conn, [rows("2025-01-01", "west")])
    assert [r[1] for r in all_rows(conn)] == ["west"]


def test_replace_all(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    load.load_daily_revenue(conn, [rows("2025-01-01"), rows("2025-01-02")])
    load.load_daily_revenue(conn, [rows("2025-01-05")], replace_all=True)
    assert [r[0] for r in all_rows(conn)] == ["2025-01-05"]


def test_load_is_atomic_on_failure(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    load.load_daily_revenue(conn, [rows("2025-01-01", revenue=1.0)])
    bad = [rows("2025-01-01", revenue=50.0), {"day": "2025-01-01", "region": "west", "orders": 1}]  # missing key
    try:
        load.load_daily_revenue(conn, bad)
    except Exception:
        pass
    assert all_rows(conn) == [("2025-01-01", "west", 1, 1.0)], "a failed load must roll back completely"


def test_watermark_roundtrip(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    assert load.get_watermark(conn) is None
    load.set_watermark(conn, "2025-01-02")
    load.set_watermark(conn, "2025-01-03")
    assert load.get_watermark(conn) == "2025-01-03"
    conn.close()
    assert load.get_watermark(load.connect(tmp_path / "x.db")) == "2025-01-03"


def test_quarantine_saved_and_idempotent(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    bad = [{"source": "orders", "reason": "status bad", "raw": {"order_id": "1", "status": "zzz"}},
           {"source": "customers", "reason": "region is required", "raw": {"customer_id": "2"}}]
    assert load.save_quarantine(conn, bad) == 2
    load.save_quarantine(conn, bad)
    n = conn.execute("select count(*) from quarantine").fetchone()[0]
    assert n == 2
    src = {r[0] for r in conn.execute("select source from quarantine")}
    assert src == {"orders", "customers"}


def test_data_persists_across_connections(tmp_path):
    conn = load.connect(tmp_path / "x.db")
    load.load_daily_revenue(conn, [rows("2025-01-01")])
    conn.close()
    again = sqlite3.connect(str(tmp_path / "x.db"))
    assert again.execute("select count(*) from daily_revenue").fetchone()[0] == 1
