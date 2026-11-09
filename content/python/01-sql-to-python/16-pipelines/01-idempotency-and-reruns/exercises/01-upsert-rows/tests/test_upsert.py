from solution import upsert


def test_replace_and_add():
    existing = [{"id": 1, "plan": "free"}, {"id": 2, "plan": "pro"}]
    incoming = [{"id": 2, "plan": "team"}, {"id": 3, "plan": "free"}]
    assert upsert(existing, incoming, "id") == [
        {"id": 1, "plan": "free"},
        {"id": 2, "plan": "team"},
        {"id": 3, "plan": "free"},
    ]


def test_idempotent():
    existing = [{"id": 1, "v": "a"}]
    incoming = [{"id": 1, "v": "b"}, {"id": 2, "v": "c"}]
    once = upsert(existing, incoming, "id")
    twice = upsert(once, incoming, "id")
    assert once == twice


def test_inputs_not_modified():
    existing = [{"id": 1, "v": "a"}]
    incoming = [{"id": 2, "v": "b"}]
    upsert(existing, incoming, "id")
    assert existing == [{"id": 1, "v": "a"}]
    assert incoming == [{"id": 2, "v": "b"}]


def test_other_key_column():
    out = upsert([{"sku": "a", "n": 1}], [{"sku": "a", "n": 2}], "sku")
    assert out == [{"sku": "a", "n": 2}]
