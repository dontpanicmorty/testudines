from typing import Annotated

import pytest
from fastapi import FastAPI, HTTPException, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from solution import install_error_handlers


class Item(BaseModel):
    quantity: int = Field(gt=0)


class Body(BaseModel):
    items: list[Item]


@pytest.fixture
def client():
    app = FastAPI()
    install_error_handlers(app)

    @app.get("/orders/{order_id}")
    def get_order(order_id: int):
        if order_id == 5:
            raise HTTPException(404, "order 5 not found")
        if order_id == 6:
            raise HTTPException(409, "order 6 conflicts")
        if order_id == 7:
            raise HTTPException(403, "forbidden")
        return {"id": order_id}

    @app.get("/list")
    def lst(limit: Annotated[int, Query(ge=1)] = 1):
        return {"limit": limit}

    @app.post("/orders")
    def create(body: Body):
        return {"ok": True}

    @app.get("/boom")
    def boom():
        raise RuntimeError("secret database password")

    return TestClient(app, raise_server_exceptions=False)


def test_404(client):
    r = client.get("/orders/5")
    assert r.status_code == 404
    assert r.json() == {"error": {"code": "not_found", "message": "order 5 not found"}}


def test_409(client):
    r = client.get("/orders/6")
    assert r.status_code == 409 and r.json()["error"]["code"] == "conflict"


def test_other_http_error(client):
    r = client.get("/orders/7")
    assert r.status_code == 403
    assert r.json() == {"error": {"code": "http_error", "message": "forbidden"}}


def test_unknown_route_uses_envelope(client):
    r = client.get("/nowhere")
    assert r.status_code == 404 and r.json()["error"]["code"] == "not_found"


def test_validation_query(client):
    r = client.get("/list?limit=0")
    err = r.json()["error"]
    assert r.status_code == 422
    assert err["code"] == "validation_error" and err["message"] == "invalid request"
    assert err["fields"] == ["query.limit"]


def test_validation_body_nested(client):
    r = client.post("/orders", json={"items": [{"quantity": 0}]})
    assert r.json()["error"]["fields"] == ["body.items.0.quantity"]


def test_path_validation(client):
    assert client.get("/orders/abc").json()["error"]["fields"] == ["path.order_id"]


def test_unexpected_is_generic_500(client):
    r = client.get("/boom")
    assert r.status_code == 500
    assert r.json() == {"error": {"code": "internal_error", "message": "internal server error"}}
    assert "secret" not in r.text


def test_success_untouched(client):
    assert client.get("/orders/1").json() == {"id": 1}
