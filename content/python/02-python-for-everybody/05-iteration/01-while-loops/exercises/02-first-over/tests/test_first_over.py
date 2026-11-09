from solution import months_to_reach


def test_no_interest():
    assert months_to_reach(100, 50, 0) == 2


def test_goal_zero():
    assert months_to_reach(0, 50, 5) == 0


def test_with_interest():
    # month 1: 100 -> 110, month 2: 210 -> 231, month 3: 331 -> 364.1
    assert months_to_reach(300, 100, 10) == 3


def test_one_month_enough():
    assert months_to_reach(10, 100, 0) == 1
