from solution import to_fahrenheit


def test_boiling():
    assert to_fahrenheit(100) == 212.0


def test_freezing():
    assert to_fahrenheit(0) == 32.0


def test_negative():
    assert to_fahrenheit(-40) == -40.0


def test_body_temperature():
    assert abs(to_fahrenheit(37) - 98.6) < 1e-9
