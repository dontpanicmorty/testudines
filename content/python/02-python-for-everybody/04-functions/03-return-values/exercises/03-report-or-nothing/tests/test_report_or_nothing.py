from solution import triangle_perimeter


def test_real_triangle():
    assert triangle_perimeter(3, 4, 5) == 12


def test_too_long_side():
    assert triangle_perimeter(1, 2, 10) is None


def test_flat_triangle_is_not_allowed():
    assert triangle_perimeter(1, 2, 3) is None


def test_longest_side_first():
    assert triangle_perimeter(9, 5, 6) == 20


def test_equilateral():
    assert triangle_perimeter(2, 2, 2) == 6
