import csv
import logging
import os
import sqlite3
from pathlib import Path

import pytest

from conftest import query
from pipeline.cli import main
from pipeline.run import run_pipeline

SMALL_EXPECTED = [
    ("2025-01-01", "east", 1, 10.0),
    ("2025-01-01", "west", 1, 25.5),
    ("2025-01-02", "unknown", 1, 7.25),
    ("2025-01-02", "west", 1, 12.0),
]


def table(db):
    return query(db, "select day, region, orders, revenue from daily_revenue order by 1, 2")


def test_full_run_end_to_end(small_data, tmp_path):
    db = tmp_path / "out.db"
    stats = run_pipeline(small_data, db)
    assert table(db) == SMALL_EXPECTED
    assert stats["orders_read"] == 6
    assert stats["orders_valid"] == 5
    assert stats["orders_quarantined"] == 1
    assert stats["items_quarantined"] == 1
    assert stats["rows_loaded"] == 4
    assert stats["watermark"] == "2025-01-02"


def test_bad_rows_land_in_quarantine_table(small_data, tmp_path):
    db = tmp_path / "out.db"
    run_pipeline(small_data, db)
    rows = query(db, "select source, reason from quarantine order by source")
    assert [r[0] for r in rows] == ["order_items", "orders"]
    assert "order_id" in dict(rows)["orders"]
    assert "quantity" in dict(rows)["order_items"]


def test_rerun_is_idempotent(small_data, tmp_path):
    db = tmp_path / "out.db"
    run_pipeline(small_data, db)
    run_pipeline(small_data, db)
    assert table(db) == SMALL_EXPECTED
    assert query(db, "select count(*) from quarantine") == [(2,)]


def test_incremental_without_state_loads_everything(small_data, tmp_path):
    db = tmp_path / "out.db"
    run_pipeline(small_data, db, incremental=True)
    assert table(db) == SMALL_EXPECTED


def test_incremental_only_touches_new_days_and_catches_late_rows(make_data, tmp_path):
    cust = [{"customer_id": 1, "region": "west"}]
    o1 = {"order_id": 1, "customer_id": 1, "placed_at": "2025-01-01 09:00:00", "status": "completed"}
    o2 = {"order_id": 2, "customer_id": 1, "placed_at": "2025-01-02 09:00:00", "status": "completed"}
    i1 = {"order_id": 1, "product_id": "P1", "quantity": 1, "unit_price": "10"}
    i2 = {"order_id": 2, "product_id": "P1", "quantity": 1, "unit_price": "20"}
    d = make_data([o1, o2], [i1, i2], cust)
    db = tmp_path / "out.db"
    run_pipeline(d, db, incremental=True)
    assert table(db) == [("2025-01-01", "west", 1, 10.0), ("2025-01-02", "west", 1, 20.0)]

    # A late order for the watermark day plus a brand-new day arrive; day 1 is tampered in the source
    o3 = {"order_id": 3, "customer_id": 1, "placed_at": "2025-01-02 20:00:00", "status": "completed"}
    o4 = {"order_id": 4, "customer_id": 1, "placed_at": "2025-01-03 09:00:00", "status": "completed"}
    i3 = {"order_id": 3, "product_id": "P1", "quantity": 1, "unit_price": "5"}
    i4 = {"order_id": 4, "product_id": "P1", "quantity": 1, "unit_price": "1"}
    i1_changed = dict(i1, unit_price="999")
    d = make_data([o1, o2, o3, o4], [i1_changed, i2, i3, i4], cust)
    stats = run_pipeline(d, db, incremental=True)
    assert table(db) == [
        ("2025-01-01", "west", 1, 10.0),      # untouched: older than the watermark
        ("2025-01-02", "west", 2, 25.0),      # watermark day is reprocessed, picks up the late order
        ("2025-01-03", "west", 1, 1.0),
    ]
    assert stats["watermark"] == "2025-01-03"
    assert stats["rows_loaded"] == 2


def test_incremental_with_nothing_new_keeps_watermark(small_data, tmp_path):
    db = tmp_path / "out.db"
    run_pipeline(small_data, db)
    run_pipeline(small_data, db, incremental=True)
    assert table(db) == SMALL_EXPECTED
    assert query(db, "select value from pipeline_state where key='watermark'") == [("2025-01-02",)]


def test_full_run_after_incremental_rebuilds_table(small_data, tmp_path):
    db = tmp_path / "out.db"
    conn = sqlite3.connect(str(db))
    conn.close()
    run_pipeline(small_data, db)
    c = sqlite3.connect(str(db))
    c.execute("insert into daily_revenue values ('1999-01-01', 'ghost', 1, 1.0)")
    c.commit()
    c.close()
    run_pipeline(small_data, db)          # full run must drop rows that are not in the source
    assert table(db) == SMALL_EXPECTED


def test_missing_input_raises_and_creates_nothing(small_data, tmp_path):
    (small_data / "order_items.csv").unlink()
    db = tmp_path / "out.db"
    with pytest.raises(FileNotFoundError):
        run_pipeline(small_data, db)
    assert not db.exists(), "read all inputs before touching the database"


def test_logging_reports_quarantine(small_data, tmp_path, caplog):
    caplog.set_level(logging.INFO, logger="pipeline")
    run_pipeline(small_data, tmp_path / "out.db")
    msgs = [r for r in caplog.records if r.name == "pipeline"]
    assert msgs, "log through logging.getLogger('pipeline')"
    assert any(r.levelno == logging.WARNING for r in msgs), "quarantined rows deserve a WARNING"
    assert any(r.levelno == logging.INFO for r in msgs)


def test_no_print_in_library(small_data, tmp_path, capsys):
    run_pipeline(small_data, tmp_path / "out.db")
    assert capsys.readouterr().out == ""


def test_cli_success_exit_code_and_data(small_data, tmp_path):
    db = tmp_path / "cli.db"
    assert main(["--data-dir", str(small_data), "--db", str(db)]) == 0
    assert table(db) == SMALL_EXPECTED


def test_cli_incremental_flag(small_data, tmp_path):
    db = tmp_path / "cli.db"
    assert main(["--data-dir", str(small_data), "--db", str(db)]) == 0
    assert main(["--data-dir", str(small_data), "--db", str(db), "--incremental"]) == 0
    assert table(db) == SMALL_EXPECTED


def test_cli_missing_file_exit_code_2(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert main(["--data-dir", str(empty), "--db", str(tmp_path / "x.db")]) == 2


def test_cli_missing_required_args_exits(tmp_path):
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2


def test_real_dataset_matches_independent_calculation(tmp_path):
    data = Path(os.environ["DOJO_DATA"])
    db = tmp_path / "real.db"
    assert main(["--data-dir", str(data), "--db", str(db)]) == 0

    def rows(name):
        with open(data / name, newline="") as f:
            return list(csv.DictReader(f))

    ok = {o["order_id"] for o in rows("orders.csv") if o["status"] in ("completed", "shipped")}
    expected = round(sum(int(i["quantity"]) * float(i["unit_price"])
                         for i in rows("order_items.csv") if i["order_id"] in ok), 2)
    got = query(db, "select round(sum(revenue), 2), sum(orders) from daily_revenue")[0]
    assert got[0] == pytest.approx(expected, abs=0.05)
    assert got[1] == len(ok)
