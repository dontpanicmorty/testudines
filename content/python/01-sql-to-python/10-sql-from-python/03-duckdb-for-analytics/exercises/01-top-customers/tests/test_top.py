import csv
from collections import defaultdict
from solution import top_customers


def write(tmp_path):
    (tmp_path / "orders.csv").write_text(
        "order_id,customer_id,placed_at,status\n"
        "1,10,2025-01-01 00:00:00,shipped\n"
        "2,10,2025-01-02 00:00:00,cancelled\n"
        "3,20,2025-01-03 00:00:00,completed\n"
        "4,30,2025-01-04 00:00:00,completed\n"
        "5,40,2025-01-05 00:00:00,cancelled\n"
    )
    (tmp_path / "order_items.csv").write_text(
        "order_id,product_id,quantity,unit_price\n"
        "1,1,2,10.00\n1,2,1,5.50\n"
        "2,1,100,10.00\n"
        "3,1,3,9.00\n3,2,1,1.50\n"
        "4,1,1,28.50\n"
        "5,1,9,99.00\n"
    )


def test_ranking_and_cancelled_excluded(tmp_path):
    write(tmp_path)
    # 10 -> 25.50 ; 20 -> 28.50 ; 30 -> 28.50 (tie, lower id first) ; 40 excluded
    assert top_customers(tmp_path, 3) == [(20, 28.5), (30, 28.5), (10, 25.5)]


def test_limit(tmp_path):
    write(tmp_path)
    assert top_customers(tmp_path, 1) == [(20, 28.5)]


def test_types(tmp_path):
    write(tmp_path)
    cid, rev = top_customers(tmp_path, 1)[0]
    assert isinstance(cid, int) and isinstance(rev, float)
