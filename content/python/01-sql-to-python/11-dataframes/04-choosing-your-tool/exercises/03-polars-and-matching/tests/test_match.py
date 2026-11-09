import numpy as np
from fixture_data import ORDERS, ITEMS, EXPECTED
from solution import top_polars, normalise


def test_polars_expected():
    assert top_polars(ORDERS, ITEMS, 4) == EXPECTED
    assert top_polars(ORDERS, ITEMS, 2) == EXPECTED[:2]


def test_polars_types_and_empty():
    cid, rev = top_polars(ORDERS, ITEMS, 1)[0]
    assert type(cid) is int and type(rev) is float
    assert top_polars([], [], 3) == []


def test_normalise_types_rounding_order():
    messy = [(np.int64(30), np.float64(30.000000001)), (np.int64(20), 30.0), (40, 29.994)]
    out = normalise(messy)
    assert out == [(20, 30.0), (30, 30.0), (40, 29.99)], out
    assert all(type(c) is int and type(r) is float for c, r in out)


def test_normalise_makes_tools_agree():
    a = [(30, 30.0), (20, 30.0)]
    b = [(20, 30.0000001), (30, 29.9999999)]
    assert normalise(a) == normalise(b)


def test_normalise_accepts_generators():
    assert normalise(iter([(2, 1.0), (1, 1.0)])) == [(1, 1.0), (2, 1.0)]
