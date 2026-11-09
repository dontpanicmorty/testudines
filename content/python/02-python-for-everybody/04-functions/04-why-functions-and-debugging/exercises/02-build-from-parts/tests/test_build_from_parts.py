from solution import walk_calories


def test_ten_thousand_steps():
    assert walk_calories(10000, 70) == 350.0


def test_needs_rounding():
    assert walk_calories(3333, 60) == 100.0


def test_rounds_to_one_place():
    assert walk_calories(1234, 71) == 43.8


def test_no_steps():
    assert walk_calories(0, 80) == 0
