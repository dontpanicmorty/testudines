from solution import party_budget


def test_basic():
    assert abs(party_budget(10, 8, 20) - 110.0) < 1e-9


def test_no_guests():
    assert abs(party_budget(0, 8, 20) - 22.0) < 1e-9


def test_free_venue():
    assert abs(party_budget(5, 10, 0) - 55.0) < 1e-9


def test_decimal_cost():
    assert abs(party_budget(4, 2.5, 10) - 22.0) < 1e-9
