import pytest

from solution import build_select


def norm(s):
    return " ".join(s.split())


def test_no_filters():
    sql, params = build_select("orders", ["id", "status"])
    assert norm(sql) == "SELECT id, status FROM orders" and params == {}


def test_filters_bound_not_inlined():
    sql, params = build_select("raw.orders", ["id"], {"region": "EU", "status": "open"})
    assert norm(sql) == "SELECT id FROM raw.orders WHERE region = %(region)s AND status = %(status)s"
    assert params == {"region": "EU", "status": "open"}
    assert "EU" not in sql


def test_params_is_a_copy():
    filters = {"a": 1}
    _, params = build_select("t", ["x"], filters)
    params["b"] = 2
    assert filters == {"a": 1}


@pytest.mark.parametrize("table", ["orders; DROP TABLE x", "a b", "1abc", "a.b.c", ""])
def test_bad_table(table):
    with pytest.raises(ValueError):
        build_select(table, ["id"])


def test_bad_column_and_filter_key():
    with pytest.raises(ValueError):
        build_select("t", ["id, (SELECT 1)"])
    with pytest.raises(ValueError):
        build_select("t", ["id"], {"a = 1 OR 1": 1})


def test_empty_columns():
    with pytest.raises(ValueError):
        build_select("t", [])
