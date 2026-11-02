import polars as pl
import pytest

from solution import top_customers


@pytest.fixture
def files(tmp_path):
    o = tmp_path / "orders.csv"
    o.write_text(
        "order_id,customer_id,placed_at,status\n"
        "1,10,2025-01-01 10:00:00,completed\n"
        "2,10,2025-01-02 10:00:00,shipped\n"
        "3,20,2025-01-03 10:00:00,completed\n"
        "4,30,2025-01-04 10:00:00,cancelled\n"
        "5,40,2025-01-05 10:00:00,refunded\n"
        "6,50,2025-01-06 10:00:00,completed\n"
    )
    i = tmp_path / "items.csv"
    i.write_text(
        "order_id,product_id,quantity,unit_price\n"
        "1,P1,2,10.00\n"
        "1,P2,1,5.50\n"
        "2,P1,1,10.00\n"
        "3,P3,3,8.50\n"
        "4,P1,100,100.00\n"
        "5,P1,100,100.00\n"
        "6,P2,3,8.50\n"
    )
    return o, i


def test_returns_lazyframe(files):
    result = top_customers(*files, 3)
    assert isinstance(result, pl.LazyFrame), "return the plan; do not call collect()"


def test_values_and_columns(files):
    df = top_customers(*files, 10).collect()
    assert df.columns == ["customer_id", "revenue"]
    assert df.rows() == [(10, 35.5), (20, 25.5), (50, 25.5)]


def test_excludes_cancelled_and_refunded(files):
    ids = top_customers(*files, 10).collect()["customer_id"].to_list()
    assert 30 not in ids and 40 not in ids


def test_tie_break_by_customer_id(files):
    df = top_customers(*files, 3).collect()
    assert df["customer_id"].to_list()[1:] == [20, 50]


def test_limit(files):
    assert top_customers(*files, 1).collect().height == 1


def test_is_lazy_reads_nothing_until_collect(tmp_path):
    # Files that do not exist are fine until the plan is collected.
    lf = top_customers(tmp_path / "nope1.csv", tmp_path / "nope2.csv", 3)
    assert isinstance(lf, pl.LazyFrame)
