from solution import flatten_event


def test_full():
    e = {"user": {"id": 7, "geo": {"country": "DE"}}, "props": {"plan": "pro"}}
    assert flatten_event(e) == {"user_id": 7, "country": "DE", "plan": "pro"}


def test_partial():
    assert flatten_event({"user": {"id": 8}}) == {"user_id": 8, "country": None, "plan": "free"}


def test_empty():
    assert flatten_event({}) == {"user_id": None, "country": None, "plan": "free"}
