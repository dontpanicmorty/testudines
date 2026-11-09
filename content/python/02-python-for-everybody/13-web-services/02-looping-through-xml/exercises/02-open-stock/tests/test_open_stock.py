from solution import open_bikes


def test_example():
    xml = '<network><station status="open"><bikes>4</bikes></station><station status="closed"><bikes>7</bikes></station></network>'
    assert open_bikes(xml) == 4


def test_all_open():
    xml = '<network>' + ''.join(f'<station status="open"><bikes>{n}</bikes></station>' for n in (1, 2, 3)) + '</network>'
    assert open_bikes(xml) == 6


def test_none_open():
    xml = '<network><station status="closed"><bikes>9</bikes></station></network>'
    assert open_bikes(xml) == 0


def test_no_stations():
    assert open_bikes("<network/>") == 0


def test_missing_status_not_counted():
    xml = '<network><station><bikes>5</bikes></station></network>'
    assert open_bikes(xml) == 0
