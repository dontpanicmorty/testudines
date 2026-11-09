from solution import Trike, Vehicle


def test_vehicle():
    assert Vehicle("Cart", 4).describe() == "Cart with 4 wheels"


def test_trike():
    t = Trike("Rosie")
    assert t.describe() == "Rosie with 3 wheels and a bell"
    assert t.wheels == 3 and t.name == "Rosie" and t.bell is True


def test_is_a_vehicle():
    assert isinstance(Trike("x"), Vehicle)


def test_parent_unchanged():
    assert Vehicle("Unicycle", 1).describe() == "Unicycle with 1 wheels"
