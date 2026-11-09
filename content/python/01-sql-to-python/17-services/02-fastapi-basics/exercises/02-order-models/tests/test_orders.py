import pytest
from fastapi.testclient import TestClient

from solution import create_app

GOOD = {"customer_id": 7, "items": [{"sku": "P003", "quantity": 2, "unit_price": 10.5}]}


def client():
    return TestClient(create_app())


def test_create_returns_201_and_exact_shape():
    r = client().post("/orders", json=GOOD)
    assert r.status_code == 201, r.text
    assert r.json() == {"order_id": 1, "customer_id": 7, "total": 21.0}


def test_total_sums_and_rounds():
    body = {"customer_id": 1, "items": [
        {"sku": "A", "quantity": 3, "unit_price": 0.1},
        {"sku": "B", "quantity": 1, "unit_price": 0.2}]}
    assert client().post("/orders", json=body).json()["total"] == 0.5


def test_ids_increment():
    c = client()
    assert c.post("/orders", json=GOOD).json()["order_id"] == 1
    assert c.post("/orders", json=GOOD).json()["order_id"] == 2


@pytest.mark.parametrize("mutate", [
    lambda b: b.pop("customer_id"),
    lambda b: b.update(customer_id="abc"),
    lambda b: b.update(items=[]),
    lambda b: b["items"][0].update(quantity=0),
    lambda b: b["items"][0].update(quantity=-3),
    lambda b: b["items"][0].update(unit_price=0),
    lambda b: b["items"][0].update(sku=""),
    lambda b: b["items"][0].pop("sku"),
])
def test_invalid_is_422(mutate):
    import copy
    body = copy.deepcopy(GOOD)
    mutate(body)
    r = client().post("/orders", json=body)
    assert r.status_code == 422, f"{body} gave {r.status_code}"


def test_invalid_does_not_consume_id():
    c = client()
    c.post("/orders", json={"customer_id": 1, "items": []})
    assert c.post("/orders", json=GOOD).json()["order_id"] == 1


def test_get_back():
    c = client()
    c.post("/orders", json=GOOD)
    r = c.get("/orders/1")
    assert r.status_code == 200 and r.json() == {"order_id": 1, "customer_id": 7, "total": 21.0}


def test_get_missing_404():
    assert client().get("/orders/5").status_code == 404
