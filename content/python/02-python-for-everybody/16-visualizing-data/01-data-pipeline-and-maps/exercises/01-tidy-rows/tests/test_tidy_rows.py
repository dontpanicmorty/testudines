from solution import clean_places


def test_example():
    assert clean_places(["Larkfield, 51.2, -1.4", "Nowhere,n/a,5"]) == [{"name": "Larkfield", "lat": 51.2, "lon": -1.4}]


def test_out_of_range():
    assert clean_places(["A,95,0", "B,0,181", "C,-90,-180"]) == [{"name": "C", "lat": -90.0, "lon": -180.0}]


def test_wrong_part_count_and_blank():
    assert clean_places(["", "A,1", "B,1,2,3", "D,1,2"]) == [{"name": "D", "lat": 1.0, "lon": 2.0}]


def test_order_kept():
    names = [r["name"] for r in clean_places(["z,1,1", "a,2,2", "m,3,3"])]
    assert names == ["z", "a", "m"]
