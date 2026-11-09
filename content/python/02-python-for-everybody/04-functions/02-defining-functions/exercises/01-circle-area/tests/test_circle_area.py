import math

from solution import circle_area


def test_unit_circle():
    assert abs(circle_area(1) - math.pi) < 1e-9


def test_radius_two():
    assert abs(circle_area(2) - 4 * math.pi) < 1e-9


def test_zero():
    assert circle_area(0) == 0


def test_decimal_radius():
    assert abs(circle_area(0.5) - 0.25 * math.pi) < 1e-9
