from solution import downstream

GRAPH = {
    "stg_orders": [],
    "stg_customers": [],
    "dim_customers": ["stg_customers"],
    "fct_orders": ["stg_orders", "dim_customers"],
    "report": ["fct_orders"],
    "other": [],
}


def test_transitive():
    assert downstream(GRAPH, "stg_orders") == {"fct_orders", "report"}


def test_diamond_and_chain():
    assert downstream(GRAPH, "stg_customers") == {"dim_customers", "fct_orders", "report"}


def test_leaf_and_isolated():
    assert downstream(GRAPH, "report") == set()
    assert downstream(GRAPH, "other") == set()


def test_excludes_self_and_does_not_mutate():
    before = {k: list(v) for k, v in GRAPH.items()}
    assert "fct_orders" not in downstream(GRAPH, "fct_orders")
    assert GRAPH == before
