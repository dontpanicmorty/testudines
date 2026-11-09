import pytest
from fastapi.testclient import TestClient

import solution
from solution import app, get_api_key, get_store


@pytest.fixture
def client():
    app.dependency_overrides[get_store] = lambda: {42: {"invoice_id": 42, "amount": 9.5}}
    app.dependency_overrides[get_api_key] = lambda: "test-key"
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_overridden_store_is_used(client):
    r = client.get("/invoices/42", headers={"X-API-Key": "test-key"})
    assert r.status_code == 200, r.text
    assert r.json() == {"invoice_id": 42, "amount": 9.5}


def test_builtin_data_not_visible_when_overridden(client):
    r = client.get("/invoices/1", headers={"X-API-Key": "test-key"})
    assert r.status_code == 404


def test_overridden_key_required(client):
    assert client.get("/invoices/42", headers={"X-API-Key": "secret"}).status_code == 401


def test_missing_key_401(client):
    assert client.get("/invoices/42").status_code == 401


def test_401_before_404(client):
    assert client.get("/invoices/9999").status_code == 401


def test_default_behaviour_without_overrides():
    app.dependency_overrides.clear()
    c = TestClient(app)
    assert c.get("/invoices/1", headers={"X-API-Key": "secret"}).json()["amount"] == 120.0
    assert c.get("/invoices/1", headers={"X-API-Key": "nope"}).status_code == 401
