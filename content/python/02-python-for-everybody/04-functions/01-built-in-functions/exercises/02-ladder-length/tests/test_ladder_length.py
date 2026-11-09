from solution import ladder_length


def test_three_four_five():
    assert ladder_length(3, 4) == 5.0


def test_five_twelve_thirteen():
    assert ladder_length(5, 12) == 13.0


def test_flat_on_the_ground():
    assert ladder_length(7, 0) == 7.0


def test_not_a_whole_number():
    assert abs(ladder_length(1, 1) - 1.4142135623730951) < 1e-12
