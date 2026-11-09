import pandas as pd
from solution import top_n_per_region


def frame():
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6],
        "region": ["west", "east", "west", "east", "west", "north"],
        "amount": [10.0, 5.0, 30.0, 50.0, 20.0, 1.0],
    })


def test_two_per_region():
    out = top_n_per_region(frame(), 2)
    assert out[["region", "order_id"]].values.tolist() == [
        ["east", 4], ["east", 2], ["north", 6], ["west", 3], ["west", 5]], out


def test_one_per_region_and_index():
    out = top_n_per_region(frame(), 1)
    assert out["order_id"].tolist() == [4, 6, 3]
    assert list(out.index) == [0, 1, 2]


def test_columns_unchanged():
    assert list(top_n_per_region(frame(), 2).columns) == ["order_id", "region", "amount"]
