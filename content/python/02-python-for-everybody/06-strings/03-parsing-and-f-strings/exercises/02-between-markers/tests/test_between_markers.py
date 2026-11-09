from solution import between


def test_single_character_markers():
    assert between("price: <12.50> only", "<", ">") == "12.50"


def test_longer_markers():
    assert between("[[x]]", "[[", "]]") == "x"


def test_missing_opener():
    assert between("no markers", "<", ">") == ""


def test_missing_closer():
    assert between("open < only", "<", ">") == ""


def test_closer_before_opener_ignored():
    assert between("> a <b>", "<", ">") == "b"
