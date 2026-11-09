import sqlite3

import pytest
from fastapi.testclient import TestClient

from solution import create_app


@pytest.fixture
def db_path(tmp_path):
    p = tmp_path / "shop.db"
    conn = sqlite3.connect(p)
    conn.execute("create table orders(order_id integer, customer_id integer, status text)")
    rows = [(i, i % 4, "shipped" if i % 2 == 0 else "completed") for i in range(1, 26)]
    conn.executemany("insert into orders values (?,?,?)", rows[::-1])  # inserted in reverse on purpose
    conn.commit()
    conn.close()
    return str(p)


def test_first_page(db_path):
    body = TestClient(create_app(db_path)).get("/orders?page_size=10").json()
    assert [r["order_id"] for r in body["items"]] == list(range(1, 11))
    assert body["total"] == 25 and body["has_next"] is True
    assert body["page"] == 1 and body["page_size"] == 10


def test_last_page_has_no_next(db_path):
    body = TestClient(create_app(db_path)).get("/orders?page=3&page_size=10").json()
    assert [r["order_id"] for r in body["items"]] == list(range(21, 26))
    assert body["has_next"] is False


def test_exact_boundary_has_next_false(db_path):
    body = TestClient(create_app(db_path)).get("/orders?page=5&page_size=5").json()
    assert len(body["items"]) == 5 and body["has_next"] is False


def test_page_beyond_end_is_empty(db_path):
    body = TestClient(create_app(db_path)).get("/orders?page=9").json()
    assert body["items"] == [] and body["total"] == 25


def test_status_filter_and_total(db_path):
    body = TestClient(create_app(db_path)).get("/orders?status=shipped&page_size=50").json()
    assert body["total"] == 12
    assert all(r["status"] == "shipped" for r in body["items"])


def test_item_shape(db_path):
    item = TestClient(create_app(db_path)).get("/orders").json()["items"][0]
    assert item == {"order_id": 1, "customer_id": 1, "status": "completed"}


@pytest.mark.parametrize("qs", ["page=0", "page_size=0", "page_size=51", "page=abc"])
def test_bad_params_422(db_path, qs):
    assert TestClient(create_app(db_path)).get(f"/orders?{qs}").status_code == 422


def test_sql_injection_is_inert(db_path):
    r = TestClient(create_app(db_path)).get("/orders", params={"status": "x' or '1'='1"})
    assert r.json()["total"] == 0


def test_health_ok_and_down(db_path, tmp_path):
    assert TestClient(create_app(db_path)).get("/health").json() == {"status": "ok"}
    bad = TestClient(create_app(str(tmp_path / "missing_dir" / "x.db")))
    r = bad.get("/health")
    assert r.status_code == 503 and r.json() == {"status": "down"}
