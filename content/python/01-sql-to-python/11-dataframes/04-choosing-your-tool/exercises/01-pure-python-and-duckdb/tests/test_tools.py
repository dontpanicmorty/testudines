from fixture_data import ORDERS, ITEMS, EXPECTED
from solution import top_python, top_duckdb


def test_python_matches_expected():
    assert top_python(ORDERS, ITEMS, 4) == EXPECTED


def test_duckdb_matches_expected():
    assert top_duckdb(ORDERS, ITEMS, 4) == EXPECTED


def test_limit_and_agreement():
    assert top_python(ORDERS, ITEMS, 2) == top_duckdb(ORDERS, ITEMS, 2) == EXPECTED[:2]


def test_types_and_empty():
    cid, rev = top_duckdb(ORDERS, ITEMS, 1)[0]
    assert type(cid) is int and type(rev) is float
    cid, rev = top_python(ORDERS, ITEMS, 1)[0]
    assert type(cid) is int and type(rev) is float
    assert top_python([], [], 3) == [] and top_duckdb([], [], 3) == []
