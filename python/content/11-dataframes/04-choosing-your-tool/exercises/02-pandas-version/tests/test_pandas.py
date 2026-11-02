from fixture_data import ORDERS, ITEMS, EXPECTED
from solution import top_pandas


def test_matches_expected():
    assert top_pandas(ORDERS, ITEMS, 4) == EXPECTED


def test_limit():
    assert top_pandas(ORDERS, ITEMS, 2) == EXPECTED[:2]


def test_plain_python_types():
    cid, rev = top_pandas(ORDERS, ITEMS, 1)[0]
    assert type(cid) is int and type(rev) is float


def test_empty():
    assert top_pandas([], [], 3) == []
    assert top_pandas(ORDERS, [], 3) == []


def test_all_cancelled():
    only = [o for o in ORDERS if o["status"] == "cancelled"]
    assert top_pandas(only, ITEMS, 3) == []
