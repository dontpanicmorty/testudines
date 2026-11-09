import os

import pytest
from fastapi.testclient import TestClient

from conftest import make_client
from revenue_api.app import create_app
from revenue_api.db import get_conn
from revenue_api.settings import Settings, get_settings


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "database": "up"}


def test_health_down_is_503(tmp_path):
    c = make_client(str(tmp_path / "no_such_dir" / "x.duckdb"))
    r = c.get("/health")
    assert r.status_code == 503
    assert r.json() == {"status": "degraded", "database": "down"}


def test_health_does_not_need_tables(tmp_path):
    assert make_client(str(tmp_path / "empty.duckdb")).get("/health").status_code == 200


def test_unknown_route_uses_envelope(client):
    r = client.get("/nowhere")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


def test_wrong_method_uses_envelope(client):
    r = client.delete("/customers/1")
    assert r.status_code == 405
    assert r.json()["error"]["code"] == "http_error"


def test_validation_error_shape(client):
    r = client.get("/customers?page=0")
    assert r.status_code == 422
    err = r.json()["error"]
    assert err["code"] == "validation_error" and err["message"] == "invalid request"
    assert err["fields"] == ["query.page"]


def test_unexpected_error_is_generic_500(db_path):
    app = create_app()

    def broken():
        raise RuntimeError("secret connection string")

    app.dependency_overrides[get_settings] = lambda: Settings(db_path=db_path)
    app.dependency_overrides[get_conn] = broken
    r = TestClient(app, raise_server_exceptions=False).get("/customers")
    assert r.status_code == 500
    assert r.json() == {"error": {"code": "internal_error", "message": "internal server error"}}
    assert "secret" not in r.text


def test_get_settings_reads_environment(monkeypatch):
    monkeypatch.setenv("REVENUE_DB_PATH", "/tmp/x.duckdb")
    monkeypatch.setenv("REVENUE_DEFAULT_PAGE_SIZE", "7")
    monkeypatch.setenv("REVENUE_MAX_PAGE_SIZE", "9")
    assert get_settings() == Settings(db_path="/tmp/x.duckdb", default_page_size=7, max_page_size=9)


def test_get_settings_defaults(monkeypatch):
    for k in ("REVENUE_DB_PATH", "REVENUE_DEFAULT_PAGE_SIZE", "REVENUE_MAX_PAGE_SIZE"):
        monkeypatch.delenv(k, raising=False)
    s = get_settings()
    assert (s.default_page_size, s.max_page_size) == (20, 100)
