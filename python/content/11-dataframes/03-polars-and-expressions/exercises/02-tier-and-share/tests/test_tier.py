import polars as pl
from solution import add_tier_and_share

DF = pl.DataFrame({
    "order_id": [1, 2, 3, 4],
    "region": ["e", "w", "e", "w"],
    "amount": [150.0, 50.0, 50.0, 10.0],
})


def test_tier():
    out = add_tier_and_share(DF)
    assert out["tier"].to_list() == ["large", "medium", "medium", "small"]


def test_share_and_shape():
    out = add_tier_and_share(DF)
    assert out["region_share"].to_list() == [0.75, 0.833, 0.25, 0.167]
    assert out.columns == ["order_id", "region", "amount", "tier", "region_share"]
    assert out["order_id"].to_list() == [1, 2, 3, 4]
