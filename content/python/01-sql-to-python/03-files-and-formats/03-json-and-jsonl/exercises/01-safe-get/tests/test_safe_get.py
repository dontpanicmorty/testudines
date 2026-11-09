from solution import dig

DOC = {"user": {"tags": ["a", "b"], "id": 0}, "props": None}


def test_found():
    assert dig(DOC, "user", "tags", 1) == "b"


def test_falsy_value_is_returned_not_default():
    assert dig(DOC, "user", "id", default=99) == 0


def test_missing_key_default():
    assert dig(DOC, "user", "plan", default="free") == "free"


def test_through_none():
    assert dig(DOC, "props", "path") is None
    assert dig(DOC, "props", "path", default="x") == "x"


def test_index_out_of_range():
    assert dig(DOC, "user", "tags", 5, default="none") == "none"


def test_no_keys_returns_obj():
    assert dig(DOC) is DOC
