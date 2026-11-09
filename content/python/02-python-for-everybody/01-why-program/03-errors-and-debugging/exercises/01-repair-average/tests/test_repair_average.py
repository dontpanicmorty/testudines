from solution import average_of_three


def test_simple():
    assert average_of_three(3, 6, 9) == 6.0


def test_equal_numbers():
    assert average_of_three(4, 4, 4) == 4.0


def test_zeros():
    assert average_of_three(0, 0, 0) == 0


def test_negative():
    assert average_of_three(-3, 0, 3) == 0
