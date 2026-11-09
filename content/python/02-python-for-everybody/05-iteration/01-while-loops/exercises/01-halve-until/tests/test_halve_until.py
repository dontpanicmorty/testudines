from solution import steps_to_one


def test_power_of_two():
    assert steps_to_one(8) == 3


def test_one_needs_no_steps():
    assert steps_to_one(1) == 0


def test_not_power_of_two():
    assert steps_to_one(10) == 3


def test_large():
    assert steps_to_one(1000) == 9
