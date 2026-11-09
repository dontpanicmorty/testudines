import polars as pl
from solution import region_revenue

DF = pl.DataFrame({
    "region": ["w", "e", "w", "e", "n", "w"],
    "status": ["paid", "paid", "paid", "cancelled", "paid", "cancelled"],
    "amount": [10.0, 20.0, 15.0, 99.0, 25.0, 1000.0],
})


def test_result():
    out = region_revenue(DF)
    assert out.columns == ["region", "n_orders", "total"]
    assert out.to_dicts() == [
        {"region": "n", "n_orders": 1, "total": 25.0},
        {"region": "w", "n_orders": 2, "total": 25.0},
        {"region": "e", "n_orders": 1, "total": 20.0},
    ], out


def test_input_unchanged():
    before = DF.clone()
    region_revenue(DF)
    assert DF.equals(before)
