from solution import trip_cost


def test_basic():
    assert abs(trip_cost(250, 8, 1.5) - 30.0) < 1e-9


def test_zero_distance():
    assert trip_cost(0, 8, 1.5) == 0


def test_hundred_km():
    assert abs(trip_cost(100, 5, 2) - 10.0) < 1e-9


def test_free_fuel():
    assert trip_cost(500, 7, 0) == 0
