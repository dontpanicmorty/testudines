import pandas as pd
import pytest
from solution import enrich_orders

ORDERS = pd.DataFrame({"order_id": [3, 1, 2], "customer_id": [20, 10, 99], "amount": [5.0, 7.5, 1.0]})
CUSTOMERS = pd.DataFrame({"customer_id": [10, 20], "first_name": ["Ada", "Linus"],
                          "last_name": ["Lovelace", "Torvalds"]})


def test_columns_and_order():
    out = enrich_orders(ORDERS, CUSTOMERS)
    assert list(out.columns) == ["order_id", "customer_id", "amount", "full_name"]
    assert out["order_id"].tolist() == [3, 1, 2]


def test_names_and_unmatched():
    out = enrich_orders(ORDERS, CUSTOMERS)
    assert out["full_name"].iloc[0] == "Linus Torvalds"
    assert out["full_name"].iloc[1] == "Ada Lovelace"
    assert pd.isna(out["full_name"].iloc[2]), "unknown customer should have a missing name"


def test_duplicate_customer_ids_raise():
    dup = pd.concat([CUSTOMERS, CUSTOMERS.iloc[[0]]], ignore_index=True)
    with pytest.raises(pd.errors.MergeError):
        enrich_orders(ORDERS, dup)


def test_inputs_not_mutated():
    o, c = ORDERS.copy(), CUSTOMERS.copy()
    enrich_orders(o, c)
    pd.testing.assert_frame_equal(o, ORDERS)
    pd.testing.assert_frame_equal(c, CUSTOMERS)
