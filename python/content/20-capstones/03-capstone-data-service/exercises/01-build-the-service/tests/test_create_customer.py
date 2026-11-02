import duckdb
import pytest

NEW = {"first_name": "Margaret", "last_name": "Hamilton", "email": "Margaret@Example.com",
       "region": "east", "plan": "pro"}


def post(client, body=NEW, key="k1"):
    headers = {"Idempotency-Key": key} if key is not None else {}
    return client.post("/customers", json=body, headers=headers)


def count(db_path):
    conn = duckdb.connect(db_path)
    try:
        return conn.execute("select count(*) from customers").fetchone()[0]
    finally:
        conn.close()


def test_create_returns_201_and_public_shape(client):
    r = post(client)
    assert r.status_code == 201, r.text
    assert r.json() == {"customer_id": 8, "first_name": "Margaret", "last_name": "Hamilton",
                        "region": "east", "plan": "pro", "signup_date": "2025-06-01"}


def test_created_customer_is_readable(client):
    post(client)
    got = client.get("/customers/8").json()
    assert got["last_name"] == "Hamilton"
    assert client.get("/customers").json()["total"] == 8


def test_email_stored_normalised(db_path, client):
    post(client)
    conn = duckdb.connect(db_path)
    assert conn.execute("select email from customers where customer_id = 8").fetchone()[0] == "margaret@example.com"
    conn.close()


@pytest.mark.parametrize("mutate", [
    lambda b: b.pop("first_name"),
    lambda b: b.update(first_name=""),
    lambda b: b.update(email="no-at-sign"),
    lambda b: b.update(plan="platinum"),
    lambda b: b.pop("region"),
])
def test_invalid_body_is_422_and_not_stored(db_path, client, mutate):
    body = dict(NEW)
    mutate(body)
    r = post(client, body)
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"
    assert count(db_path) == 7


def test_missing_idempotency_key_is_422(client):
    r = post(client, key=None)
    assert r.status_code == 422 and "header.idempotency-key" in r.json()["error"]["fields"]


def test_duplicate_email_is_409_case_insensitive(db_path, client):
    r = post(client, dict(NEW, email="ADA@example.com"))
    assert r.status_code == 409
    assert r.json()["error"]["code"] == "conflict"
    assert count(db_path) == 7


def test_replay_returns_same_response_and_creates_nothing(db_path, client):
    a = post(client)
    b = post(client)
    assert a.status_code == b.status_code == 201
    assert a.json() == b.json()
    assert count(db_path) == 8


def test_many_retries_one_row(db_path, client):
    for _ in range(5):
        post(client)
    assert count(db_path) == 8


def test_replay_survives_a_new_app_instance(db_path, factory):
    first = post(factory())
    second = post(factory())            # fresh app, same database file
    assert first.json() == second.json()
    assert count(db_path) == 8


def test_same_key_different_body_is_409(db_path, client):
    post(client)
    r = post(client, dict(NEW, first_name="Someone Else", email="else@example.com"))
    assert r.status_code == 409
    assert count(db_path) == 8


def test_different_keys_create_different_customers(client):
    a = post(client, key="a")
    b = post(client, dict(NEW, email="other@example.com"), key="b")
    assert (a.json()["customer_id"], b.json()["customer_id"]) == (8, 9)


def test_invalid_request_does_not_reserve_the_key(client):
    assert post(client, dict(NEW, plan="nope"), key="shared").status_code == 422
    assert post(client, key="shared").status_code == 201


def test_failed_duplicate_email_does_not_reserve_key(client):
    assert post(client, dict(NEW, email="ada@example.com"), key="k").status_code == 409
    assert post(client, key="k").status_code == 201
