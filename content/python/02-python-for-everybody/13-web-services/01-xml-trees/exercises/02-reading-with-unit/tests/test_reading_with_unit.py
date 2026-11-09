from solution import parse_reading


def test_basic():
    assert parse_reading('<reading sensor="T3"><temp unit="C">21.5</temp></reading>') == ("T3", 21.5, "C")


def test_other_unit():
    assert parse_reading('<reading sensor="Z9"><temp unit="F">70</temp></reading>') == ("Z9", 70.0, "F")


def test_negative_value():
    result = parse_reading('<reading sensor="N1"><temp unit="C">-4.25</temp></reading>')
    assert result == ("N1", -4.25, "C")
    assert isinstance(result[1], float)
