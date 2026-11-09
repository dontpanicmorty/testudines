from fastapi.testclient import TestClient

from solution import create_app

BODY = {"customer_id": 1, "amount": 25}


def client():
    return TestClient(create_app())


def post(c, body=BODY, key="k1"):
    headers = {"Idempotency-Key": key} if key is not None else {}
    return c.post("/payments", json=body, headers=headers)


def test_create():
    r = post(client())
    assert r.status_code == 201
    assert r.json() == {"payment_id": 1, "customer_id": 1, "amount": 25}


def test_replay_same_response_no_new_row():
    c = client()
    a, b = post(c), post(c)
    assert a.status_code == b.status_code == 201
    assert a.json() == b.json()
    assert len(c.get("/payments").json()["items"]) == 1


def test_many_retries_one_payment():
    c = client()
    for _ in range(5):
        post(c)
    assert len(c.get("/payments").json()["items"]) == 1


def test_same_key_different_body_409():
    c = client()
    post(c)
    r = post(c, {"customer_id": 1, "amount": 99})
    assert r.status_code == 409
    assert len(c.get("/payments").json()["items"]) == 1


def test_different_keys_make_different_payments():
    c = client()
    post(c, key="a")
    r = post(c, key="b")
    assert r.json()["payment_id"] == 2


def test_missing_key_422():
    assert post(client(), key=None).status_code == 422


def test_invalid_body_422_and_key_not_reserved():
    c = client()
    assert post(c, {"customer_id": 1, "amount": -5}).status_code == 422
    r = post(c, {"customer_id": 1, "amount": 10})
    assert r.status_code == 201 and r.json()["amount"] == 10


def test_apps_do_not_share_state():
    a, b = client(), client()
    post(a)
    assert b.get("/payments").json() == {"items": []}
