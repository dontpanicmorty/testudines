from solution import normalise_names


def test_basic():
    assert normalise_names(["  aDA lovelace ", "GRACE hopper", "   ", None]) == ["Ada Lovelace", "Grace Hopper"]


def test_empty():
    assert normalise_names([]) == []
    assert normalise_names([None, ""]) == []
