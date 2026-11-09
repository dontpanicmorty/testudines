import polars as pl
from solution import daily_revenue


def write(tmp_path):
    (tmp_path / "orders.csv").write_text(
        "order_id,customer_id,placed_at,status\n"
        "1,10,2025-01-02 08:00:00,shipped\n"
        "2,11,2025-01-02 23:59:00,completed\n"
        "3,12,2025-01-01 10:00:00,cancelled\n"
        "4,13,2025-01-03 00:00:00,completed\n"
    )
    (tmp_path / "order_items.csv").write_text(
        "order_id,product_id,quantity,unit_price\n"
        "1,1,2,10.25\n1,2,1,0.10\n"
        "2,1,1,5.00\n"
        "3,1,50,100.00\n"
        "4,1,3,1.10\n"
    )
    return tmp_path / "orders.csv", tmp_path / "order_items.csv"


def test_daily(tmp_path):
    o, i = write(tmp_path)
    out = daily_revenue(o, i)
    assert out.columns == ["day", "revenue"]
    assert out.to_dicts() == [
        {"day": "2025-01-02", "revenue": 25.6},
        {"day": "2025-01-03", "revenue": 3.3},
    ], out


def test_returns_eager_frame(tmp_path):
    o, i = write(tmp_path)
    assert isinstance(daily_revenue(o, i), pl.DataFrame)
