import duckdb
import pytest
from solution import run_models

MODELS = {
    "report": "SELECT c.cust, t.total FROM {{ ref('totals') }} t JOIN {{ ref('customers') }} c USING (cust)",
    "totals": "SELECT cust, SUM(amt) AS total FROM {{ ref('orders') }} GROUP BY cust",
    "customers": "SELECT * FROM (VALUES ('a'), ('b')) t(cust)",
    "orders": "SELECT * FROM (VALUES ('a', 1), ('a', 2), ('b', 5)) t(cust, amt)",
}


def test_builds_in_dependency_order():
    con = duckdb.connect()
    order = run_models(con, MODELS)
    assert sorted(order) == sorted(MODELS)
    pos = {n: i for i, n in enumerate(order)}
    assert pos["orders"] < pos["totals"] < pos["report"]
    assert pos["customers"] < pos["report"]


def test_result_tables():
    con = duckdb.connect()
    run_models(con, MODELS)
    assert con.execute("SELECT cust, total FROM report ORDER BY cust").fetchall() == [("a", 3), ("b", 5)]


def test_idempotent():
    con = duckdb.connect()
    run_models(con, MODELS)
    run_models(con, MODELS)
    assert con.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 3
    assert con.execute("SELECT COUNT(*) FROM report").fetchone()[0] == 2


def test_unknown_ref():
    with pytest.raises(KeyError):
        run_models(duckdb.connect(), {"a": "SELECT * FROM {{ ref('nope') }}"})


def test_cycle():
    with pytest.raises(ValueError):
        run_models(duckdb.connect(), {"a": "SELECT * FROM {{ ref('b') }}", "b": "SELECT * FROM {{ ref('a') }}"})
