from solution import revenue_by_product


def test_totals(tmp_path):
    p = tmp_path / "l.csv"
    p.write_text(
        "order_id,product_id,quantity,unit_price\n1,P1,2,5.0\n1,P2,3,1.5\n2,P1,1,5.0\n",
        encoding="utf-8",
    )
    assert revenue_by_product(p) == {"P1": 15.0, "P2": 4.5}


def test_single_line(tmp_path):
    p = tmp_path / "l.csv"
    p.write_text("order_id,product_id,quantity,unit_price\n1,P1,2,5.0\n", encoding="utf-8")
    assert revenue_by_product(p) == {"P1": 10.0}


def test_header_only(tmp_path):
    p = tmp_path / "l.csv"
    p.write_text("order_id,product_id,quantity,unit_price\n", encoding="utf-8")
    assert revenue_by_product(p) == {}
