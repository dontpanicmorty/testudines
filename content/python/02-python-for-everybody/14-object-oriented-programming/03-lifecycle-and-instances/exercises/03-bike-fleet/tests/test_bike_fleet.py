from solution import Bike, Fleet


def make():
    f = Fleet()
    bikes = [Bike("B2"), Bike("B1"), Bike("B3")]
    for b in bikes:
        f.add(b)
    return f, bikes


def test_available_sorted():
    f, _ = make()
    assert f.available() == ["B1", "B2", "B3"]


def test_rent_and_conflict():
    f, bikes = make()
    assert f.rent("B1") is True
    assert f.rent("B1") is False
    assert f.available() == ["B2", "B3"]
    assert bikes[1].rented is True


def test_unknown_ids():
    f, _ = make()
    assert f.rent("nope") is False
    assert f.bring_back("nope") is False


def test_bring_back():
    f, _ = make()
    assert f.bring_back("B2") is False
    f.rent("B2")
    assert f.bring_back("B2") is True
    assert f.available() == ["B1", "B2", "B3"]


def test_new_bike_starts_free():
    assert Bike("Z").rented is False
