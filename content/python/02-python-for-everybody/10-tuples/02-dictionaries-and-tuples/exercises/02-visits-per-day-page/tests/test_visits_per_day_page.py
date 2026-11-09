from solution import visit_counts


def test_basic():
    log = [("mon", "home"), ("mon", "shop"), ("mon", "home")]
    assert visit_counts(log) == {("mon", "home"): 2, ("mon", "shop"): 1}


def test_empty():
    assert visit_counts([]) == {}


def test_order_matters():
    result = visit_counts([("a", "b"), ("b", "a")])
    assert result == {("a", "b"): 1, ("b", "a"): 1}


def test_same_page_different_day():
    result = visit_counts([("mon", "x"), ("tue", "x"), ("tue", "x")])
    assert result[("tue", "x")] == 2
    assert result[("mon", "x")] == 1


def test_lookup_with_tuple_key():
    assert visit_counts([("d", "p")])[("d", "p")] == 1
