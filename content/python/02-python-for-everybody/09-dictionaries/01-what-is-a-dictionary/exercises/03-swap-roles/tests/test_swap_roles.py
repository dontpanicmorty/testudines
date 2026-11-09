from solution import members_by_club


def test_basic():
    joined = {"Ana": "chess", "Ben": "drama", "Cy": "chess"}
    assert members_by_club(joined) == {"chess": ["Ana", "Cy"], "drama": ["Ben"]}


def test_empty():
    assert members_by_club({}) == {}


def test_sorted_members():
    joined = {"Zoe": "a", "Amy": "a", "Max": "a"}
    assert members_by_club(joined) == {"a": ["Amy", "Max", "Zoe"]}


def test_input_unchanged():
    joined = {"Ana": "chess"}
    members_by_club(joined)
    assert joined == {"Ana": "chess"}


def test_single_member_clubs():
    assert members_by_club({"x": "p", "y": "q"}) == {"p": ["x"], "q": ["y"]}
