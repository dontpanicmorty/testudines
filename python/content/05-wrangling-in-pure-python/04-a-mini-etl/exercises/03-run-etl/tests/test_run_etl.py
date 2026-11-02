import csv
import sqlite3

from solution import run_etl

SRC = (
    "order_id,customer_id,sku,quantity,unit_price\n"
    "A1,1,x-100,2,5.00\n"
    "A1,1,y-200,1,12.50\n"
    "A2,2,x-100,0,5.00\n"
    "A3,two,z-300,1,1.00\n"
    "A4,2,y-200,3,12.50\n"
)


def setup(tmp_path, text=SRC):
    src = tmp_path / "lines.csv"
    src.write_text(text, encoding="utf-8")
    return src, tmp_path / "wh.db", tmp_path / "rejects.csv"


def rows(db, sql):
    conn = sqlite3.connect(db)
    try:
        return conn.execute(sql).fetchall()
    finally:
        conn.close()


def test_counts_and_tables(tmp_path):
    src, db, rej = setup(tmp_path)
    assert run_etl(src, db, rej) == {"read": 5, "loaded": 3, "rejected": 2}
    assert rows(db, "SELECT order_id, sku, customer_id, quantity, unit_price FROM order_lines ORDER BY 1, 2") == [
        ("A1", "X-100", 1, 2, "5.00"),
        ("A1", "Y-200", 1, 1, "12.50"),
        ("A4", "Y-200", 2, 3, "12.50"),
    ]
    assert rows(db, "SELECT customer_id, line_count, revenue FROM customer_totals ORDER BY 1") == [
        (1, 2, "22.50"),
        (2, 1, "37.50"),
    ]


def test_rejects_file(tmp_path):
    src, db, rej = setup(tmp_path)
    run_etl(src, db, rej)
    with open(rej, newline="", encoding="utf-8") as f:
        out = list(csv.DictReader(f))
    assert [r["line"] for r in out] == ["4", "5"]
    assert all(r["reason"] for r in out)


def test_idempotent(tmp_path):
    src, db, rej = setup(tmp_path)
    first = run_etl(src, db, rej)
    before = rows(db, "SELECT * FROM order_lines ORDER BY 1, 2"), rows(db, "SELECT * FROM customer_totals ORDER BY 1")
    second = run_etl(src, db, rej)
    after = rows(db, "SELECT * FROM order_lines ORDER BY 1, 2"), rows(db, "SELECT * FROM customer_totals ORDER BY 1")
    assert first == second
    assert before == after


def test_last_duplicate_wins_and_totals_not_doubled(tmp_path):
    text = "order_id,customer_id,sku,quantity,unit_price\nA1,1,x,1,10.00\nA1,1,X,3,10.00\n"
    src, db, rej = setup(tmp_path, text)
    assert run_etl(src, db, rej) == {"read": 2, "loaded": 1, "rejected": 0}
    assert rows(db, "SELECT quantity FROM order_lines") == [(3,)]
    assert rows(db, "SELECT line_count, revenue FROM customer_totals") == [(1, "30.00")]


def test_empty_rejects_still_written(tmp_path):
    text = "order_id,customer_id,sku,quantity,unit_price\nA1,1,x,1,1.00\n"
    src, db, rej = setup(tmp_path, text)
    run_etl(src, db, rej)
    assert rej.read_text(encoding="utf-8").strip() == "line,reason"


def test_rerun_with_changed_file_refreshes_totals(tmp_path):
    src, db, rej = setup(tmp_path)
    run_etl(src, db, rej)
    src.write_text(
        "order_id,customer_id,sku,quantity,unit_price\nA1,1,X-100,1,5.00\n", encoding="utf-8"
    )
    run_etl(src, db, rej)
    assert rows(db, "SELECT customer_id, line_count, revenue FROM customer_totals") == [(1, 1, "5.00")]
