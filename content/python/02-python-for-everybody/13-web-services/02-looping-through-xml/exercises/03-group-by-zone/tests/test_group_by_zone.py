from solution import stations_by_zone


def test_example():
    xml = '<city><zone name="North"><station>Mill Lane</station><station>Hill Top</station></zone><zone name="South"><station>Quay Street</station></zone></city>'
    assert stations_by_zone(xml) == {"North": ["Mill Lane", "Hill Top"], "South": ["Quay Street"]}


def test_empty_zone():
    xml = '<city><zone name="East"></zone></city>'
    assert stations_by_zone(xml) == {"East": []}


def test_no_zones():
    assert stations_by_zone("<city/>") == {}


def test_stations_outside_zones_ignored():
    xml = '<city><station>Loose</station><zone name="A"><station>X</station></zone></city>'
    assert stations_by_zone(xml) == {"A": ["X"]}
