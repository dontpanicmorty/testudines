import sqlite3
import pytest
from solution import search_products


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE products (product_id INTEGER, name TEXT, category TEXT, unit_price REAL)")
    c.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", [
        (1, "Hammer", "tools", 15.0), (2, "Saw", "tools", 25.5),
        (3, "Pen", "office", 2.0), (4, "O'Reilly Mug", "office", 9.0),
    ])
    return c


def names(rows):
    return [r["name"] for r in rows]


def test_no_filters_sorted_by_name(conn):
    assert names(search_products(conn)) == ["Hammer", "O'Reilly Mug", "Pen", "Saw"]


def test_category_and_price(conn):
    rows = search_products(conn, category="tools", min_price=20)
    assert names(rows) == ["Saw"]
    assert set(rows[0]) == {"product_id", "name", "category", "unit_price"}


def test_sort_desc(conn):
    assert names(search_products(conn, sort_by="unit_price", direction="DESC"))[0] == "Saw"


def test_value_with_quote_or_injection(conn):
    assert search_products(conn, category="x' OR '1'='1") == []


@pytest.mark.parametrize("bad", ["name; DROP TABLE products", "price", ""])
def test_bad_sort_rejected(conn, bad):
    with pytest.raises(ValueError):
        search_products(conn, sort_by=bad)
    assert conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 4


def test_bad_direction_rejected(conn):
    with pytest.raises(ValueError):
        search_products(conn, direction="sideways")
