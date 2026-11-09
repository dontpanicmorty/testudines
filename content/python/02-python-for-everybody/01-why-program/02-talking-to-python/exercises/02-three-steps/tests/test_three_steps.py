from solution import run_steps


def test_one():
    assert run_steps(1) == 9


def test_ten():
    assert run_steps(10) == 27


def test_zero():
    assert run_steps(0) == 7


def test_negative():
    assert run_steps(-5) == -3
