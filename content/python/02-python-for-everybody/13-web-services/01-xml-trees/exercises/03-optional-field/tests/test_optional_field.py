from solution import field_or_default


def test_present():
    assert field_or_default("<a><b>hi</b></a>", "b", "?") == "hi"


def test_missing_child():
    assert field_or_default("<a><b>hi</b></a>", "c", "?") == "?"


def test_empty_child():
    assert field_or_default("<a><b></b></a>", "b", "?") == "?"


def test_self_closing_child():
    assert field_or_default("<a><b/></a>", "b", "none") == "none"


def test_default_can_be_anything():
    assert field_or_default("<a></a>", "b", 0) == 0
