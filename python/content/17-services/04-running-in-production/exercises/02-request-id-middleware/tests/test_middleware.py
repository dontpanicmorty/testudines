import logging

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel

from solution import add_request_id


class Body(BaseModel):
    n: int


@pytest.fixture
def client():
    app = FastAPI()
    add_request_id(app)

    @app.get("/ping")
    def ping(request: Request):
        return {"request_id": request.state.request_id}

    @app.post("/echo")
    def echo(body: Body):
        return {"n": body.n}

    @app.get("/boom")
    def boom():
        raise RuntimeError("bug")

    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def records(caplog):
    caplog.set_level(logging.INFO, logger="access")
    return caplog


def access(records):
    return [r for r in records.records if r.name == "access"]


def test_incoming_id_reused_everywhere(client):
    r = client.get("/ping", headers={"X-Request-ID": "abc"})
    assert r.headers["x-request-id"] == "abc"
    assert r.json() == {"request_id": "abc"}


def test_generated_id_when_missing_and_unique(client):
    a = client.get("/ping").headers["x-request-id"]
    b = client.get("/ping").headers["x-request-id"]
    assert a and b and a != b


def test_empty_header_treated_as_missing(client):
    r = client.get("/ping", headers={"X-Request-ID": ""})
    assert r.headers["x-request-id"] != ""


def test_header_on_404_and_422(client):
    assert client.get("/nope", headers={"X-Request-ID": "z"}).headers["x-request-id"] == "z"
    r = client.post("/echo", json={"n": "x"}, headers={"X-Request-ID": "q"})
    assert r.status_code == 422 and r.headers["x-request-id"] == "q"


def test_one_log_record_per_request(client, records):
    client.get("/ping", headers={"X-Request-ID": "abc"})
    recs = access(records)
    assert len(recs) == 1
    r = recs[0]
    assert r.levelno == logging.INFO and r.getMessage() == "request"
    f = r.fields
    assert f["request_id"] == "abc" and f["method"] == "GET" and f["path"] == "/ping"
    assert f["status"] == 200 and isinstance(f["duration_ms"], float) and f["duration_ms"] >= 0


def test_log_status_for_validation_error(client, records):
    client.post("/echo", json={"n": "x"})
    assert access(records)[0].fields["status"] == 422


def test_unexpected_error_logged_as_500(client, records):
    r = client.get("/boom", headers={"X-Request-ID": "b1"})
    assert r.status_code == 500
    recs = access(records)
    assert len(recs) == 1 and recs[0].fields["status"] == 500 and recs[0].fields["request_id"] == "b1"


def test_each_request_gets_its_own_record(client, records):
    client.get("/ping")
    client.get("/ping")
    assert len(access(records)) == 2
