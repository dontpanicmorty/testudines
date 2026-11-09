import csv
import sqlite3

import pytest

ORDER_COLS = ["order_id", "customer_id", "placed_at", "status"]
ITEM_COLS = ["order_id", "product_id", "quantity", "unit_price"]
CUSTOMER_COLS = ["customer_id", "first_name", "last_name", "email", "region", "plan", "signup_date"]


def _write(path, cols, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


@pytest.fixture
def make_data(tmp_path):
    def build(orders, items, customers, name="data"):
        d = tmp_path / name
        d.mkdir(exist_ok=True)
        _write(d / "orders.csv", ORDER_COLS, orders)
        _write(d / "order_items.csv", ITEM_COLS, items)
        _write(d / "customers.csv", CUSTOMER_COLS, customers)
        return d
    return build


@pytest.fixture
def small_data(make_data):
    orders = [
        {"order_id": 1, "customer_id": 1, "placed_at": "2025-01-01 09:00:00", "status": "completed"},
        {"order_id": 2, "customer_id": 2, "placed_at": "2025-01-01 10:00:00", "status": "shipped"},
        {"order_id": 3, "customer_id": 1, "placed_at": "2025-01-02 11:00:00", "status": "cancelled"},
        {"order_id": 4, "customer_id": 1, "placed_at": "2025-01-02 12:00:00", "status": "completed"},
        {"order_id": 5, "customer_id": 99, "placed_at": "2025-01-02 13:00:00", "status": "completed"},
        {"order_id": "x", "customer_id": 1, "placed_at": "2025-01-02 14:00:00", "status": "completed"},
    ]
    items = [
        {"order_id": 1, "product_id": "P1", "quantity": 2, "unit_price": "10.00"},
        {"order_id": 1, "product_id": "P2", "quantity": 1, "unit_price": "5.50"},
        {"order_id": 2, "product_id": "P1", "quantity": 1, "unit_price": "10.00"},
        {"order_id": 3, "product_id": "P1", "quantity": 9, "unit_price": "10.00"},
        {"order_id": 4, "product_id": "P3", "quantity": 3, "unit_price": "4.00"},
        {"order_id": 5, "product_id": "P3", "quantity": 1, "unit_price": "7.25"},
        {"order_id": 4, "product_id": "P3", "quantity": 0, "unit_price": "4.00"},
    ]
    customers = [
        {"customer_id": 1, "region": "West"},
        {"customer_id": 2, "region": "east"},
    ]
    return make_data(orders, items, customers)


def query(db_path, sql, params=()):
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()
