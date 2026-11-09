from solution import hours_and_minutes


def test_over_an_hour():
    assert hours_and_minutes(135) == (2, 15)


def test_under_an_hour():
    assert hours_and_minutes(45) == (0, 45)


def test_exact_hours():
    assert hours_and_minutes(180) == (3, 0)


def test_zero():
    assert hours_and_minutes(0) == (0, 0)
