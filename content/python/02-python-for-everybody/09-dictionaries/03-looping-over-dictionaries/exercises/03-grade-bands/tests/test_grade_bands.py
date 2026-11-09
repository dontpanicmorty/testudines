from solution import bands


def test_basic():
    result = bands({"Ana": 95, "Ben": 82, "Cy": 90, "Dee": 40})
    assert result == {"A": ["Ana", "Cy"], "B": ["Ben"], "C": ["Dee"]}


def test_boundaries():
    assert bands({"x": 90, "y": 89, "z": 80}) == {"A": ["x"], "B": ["y", "z"]}


def test_empty_bands_absent():
    assert bands({"x": 10}) == {"C": ["x"]}


def test_empty_input():
    assert bands({}) == {}


def test_names_sorted():
    assert bands({"Zed": 99, "Amy": 91}) == {"A": ["Amy", "Zed"]}
