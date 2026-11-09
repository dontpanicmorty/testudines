from solution import register


def test_basic():
    assert register(["Cy"], ["Ana", "Cy"]) == ["Ana", "Cy"]


def test_changes_original():
    r = ["Bo"]
    result = register(r, ["Al"])
    assert result is r
    assert r == ["Al", "Bo"]


def test_duplicates_in_newcomers():
    assert register([], ["Zed", "Zed", "Amy"]) == ["Amy", "Zed"]


def test_nothing_new():
    assert register(["b", "a"], []) == ["a", "b"]
