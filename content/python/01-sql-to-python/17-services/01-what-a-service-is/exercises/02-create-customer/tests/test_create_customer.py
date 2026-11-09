import copy

from solution import create_customer


def test_success_normalises_and_returns_201():
    store = {}
    status, body = create_customer(store, {"name": "Ada", "email": " Ada@Example.com "})
    assert status == 201, f"expected 201, got {status}"
    assert body == {"id": 1, "name": "Ada", "email": "ada@example.com"}
    assert store[1] == body


def test_missing_name_422():
    assert create_customer({}, {"email": "a@b.co"})[0] == 422


def test_blank_name_422():
    assert create_customer({}, {"name": "  ", "email": "a@b.co"})[0] == 422


def test_bad_email_422_and_not_saved():
    store = {}
    status, body = create_customer(store, {"name": "Ada", "email": "not-an-email"})
    assert status == 422 and "error" in body
    assert store == {}, "invalid customer must not be stored"


def test_missing_email_422():
    assert create_customer({}, {"name": "Ada"})[0] == 422


def test_duplicate_is_409_case_insensitive():
    store = {}
    create_customer(store, {"name": "Ada", "email": "ada@example.com"})
    before = copy.deepcopy(store)
    status, body = create_customer(store, {"name": "Other", "email": "  ADA@example.com"})
    assert status == 409 and "error" in body
    assert store == before


def test_ids_use_max_plus_one_not_length():
    store = {1: {"id": 1, "name": "A", "email": "a@x.io"}, 5: {"id": 5, "name": "B", "email": "b@x.io"}}
    status, body = create_customer(store, {"name": "C", "email": "c@x.io"})
    assert status == 201 and body["id"] == 6, f"got id {body.get('id')}"
