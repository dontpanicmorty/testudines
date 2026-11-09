from solution import build_query


def test_defaults():
    assert build_query("orders") == "SELECT * FROM analytics.orders"


def test_schema_limit():
    assert build_query("orders", schema="raw", limit=10) == "SELECT * FROM raw.orders LIMIT 10"


def test_filters_sorted():
    assert build_query("orders", status="paid", region="EU") == (
        "SELECT * FROM analytics.orders WHERE region = 'EU' AND status = 'paid'"
    )


def test_all_together():
    assert build_query("t", limit=5, a="x") == "SELECT * FROM analytics.t WHERE a = 'x' LIMIT 5"


def test_limit_zero_is_kept():
    assert build_query("t", limit=0).endswith("LIMIT 0")
