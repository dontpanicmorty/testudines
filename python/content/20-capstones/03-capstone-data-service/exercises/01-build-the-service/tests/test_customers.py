import csv
import os
from pathlib import Path

import duckdb
import pytest

from conftest import make_client


def ids(body):
    return [c["customer_id"] for c in body["items"]]


def test_list_default(client):
    body = client.get("/customers").json()
    assert ids(body) == [1, 2, 3, 4, 5, 6, 7] and body["total"] == 7


def test_email_is_never_exposed(client):
    body = client.get("/customers").json()
    assert all("email" not in c for c in body["items"])
    assert "email" not in client.get("/customers/1").json()
    assert "@" not in client.get("/customers").text


def test_item_shape(client):
    assert client.get("/customers/1").json() == {
        "customer_id": 1, "first_name": "Ada", "last_name": "Lovelace",
        "region": "west", "plan": "pro", "signup_date": "2024-01-05"}


def test_filters(client):
    assert ids(client.get("/customers?region=west").json()) == [1, 3, 5, 7]
    assert ids(client.get("/customers?plan=pro").json()) == [1, 4, 6, 7]
    assert ids(client.get("/customers?region=west&plan=pro").json()) == [1, 7]


def test_total_counts_filtered_rows_not_page(client):
    body = client.get("/customers?plan=pro&page_size=2").json()
    assert body["total"] == 4 and len(body["items"]) == 2 and body["has_next"] is True


def test_pages_do_not_overlap(client):
    first = ids(client.get("/customers?page=1&page_size=3").json())
    second = ids(client.get("/customers?page=2&page_size=3").json())
    third = ids(client.get("/customers?page=3&page_size=3").json())
    assert first == [1, 2, 3] and second == [4, 5, 6] and third == [7]


def test_get_one_missing_404(client):
    r = client.get("/customers/999")
    assert r.status_code == 404
    assert r.json()["error"] == {"code": "not_found", "message": "customer 999 not found"}


def test_get_one_non_integer_422(client):
    r = client.get("/customers/abc")
    assert r.status_code == 422 and r.json()["error"]["fields"] == ["path.customer_id"]


def test_real_customers_csv_pagination(tmp_path):
    csv_path = Path(os.environ["DOJO_DATA"]) / "customers.csv"
    path = str(tmp_path / "real.duckdb")
    conn = duckdb.connect(path)
    conn.execute("create table customers as select * from read_csv_auto(?)", [str(csv_path)])
    conn.close()
    with open(csv_path, newline="") as f:
        expected = sum(1 for _ in csv.DictReader(f))
    c = make_client(path)
    seen, page = [], 1
    while True:
        body = c.get(f"/customers?page={page}&page_size=50").json()
        seen += ids(body)
        if not body["has_next"]:
            break
        page += 1
    assert body["total"] == expected == len(seen) == len(set(seen))
    assert seen == sorted(seen)
