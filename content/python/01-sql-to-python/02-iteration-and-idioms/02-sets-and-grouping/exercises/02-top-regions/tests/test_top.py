from solution import top_regions

CS = [{"region": "eu"}, {"region": "EU "}, {"region": "us"}, {"region": None}, {},
      {"region": "apac"}, {"region": "US"}, {"region": "  "}]


def test_top2():
    assert top_regions(CS, 2) == [("EU", 2), ("US", 2)]


def test_all():
    assert top_regions(CS, 5) == [("EU", 2), ("US", 2), ("APAC", 1)]


def test_empty():
    assert top_regions([], 3) == []
