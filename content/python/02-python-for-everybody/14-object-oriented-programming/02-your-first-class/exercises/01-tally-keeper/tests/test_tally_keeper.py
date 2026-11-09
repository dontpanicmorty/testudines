from solution import Tally


def test_starts_at_zero():
    assert Tally().count == 0


def test_add_default_and_amount():
    t = Tally()
    t.add()
    t.add(4)
    assert t.count == 5


def test_reset():
    t = Tally()
    t.add(9)
    t.reset()
    assert t.count == 0


def test_instances_independent():
    a, b = Tally(), Tally()
    a.add(3)
    assert b.count == 0
