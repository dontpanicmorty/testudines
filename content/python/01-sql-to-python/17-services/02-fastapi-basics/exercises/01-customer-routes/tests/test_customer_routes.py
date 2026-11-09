from fastapi.testclient import TestClient

from solution import create_app

ROWS = [
    {"customer_id": 1, "name": "Ada", "region": "west"},
    {"customer_id": 2, "name": "Linus", "region": "east"},
    {"customer_id": 3, "name": "Grace", "region": "west"},
    {"customer_id": 4, "name": "Alan", "region": "west"},
]


def client():
    return TestClient(create_app(ROWS))


def test_get_one():
    r = client().get("/customers/2")
    assert r.status_code == 200
    assert r.json()["name"] == "Linus"


def test_missing_is_404():
    assert client().get("/customers/99").status_code == 404


def test_non_int_is_422():
    assert client().get("/customers/abc").status_code == 422


def test_list_default_returns_all_with_total():
    body = client().get("/customers").json()
    assert body["total"] == 4 and len(body["items"]) == 4


def test_filter_region_total_after_filter():
    body = client().get("/customers?region=west&limit=2").json()
    assert body["total"] == 3
    assert [c["customer_id"] for c in body["items"]] == [1, 3]


def test_offset():
    body = client().get("/customers?region=west&limit=2&offset=2").json()
    assert [c["customer_id"] for c in body["items"]] == [4]


def test_limit_bounds_422():
    c = client()
    assert c.get("/customers?limit=0").status_code == 422
    assert c.get("/customers?limit=101").status_code == 422


def test_negative_offset_422():
    assert client().get("/customers?offset=-1").status_code == 422


def test_apps_are_independent():
    a = TestClient(create_app(ROWS[:1]))
    b = TestClient(create_app(ROWS))
    assert a.get("/customers").json()["total"] == 1
    assert b.get("/customers").json()["total"] == 4
