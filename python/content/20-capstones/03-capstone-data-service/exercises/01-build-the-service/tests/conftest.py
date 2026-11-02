from datetime import date

import duckdb
import pytest
from fastapi.testclient import TestClient

from revenue_api.app import create_app
from revenue_api.settings import Settings, get_settings, get_today

REGIONS = ["east", "west"]


def seed(path):
    conn = duckdb.connect(str(path))
    conn.execute("create table daily_revenue(day date, region varchar, orders integer, revenue double)")
    rows = []
    for d in range(1, 6):
        for i, region in enumerate(REGIONS):
            rows.append((date(2025, 1, d), region, d + i, d * 100.0 + i * 10 + 0.005))
    conn.executemany("insert into daily_revenue values (?, ?, ?, ?)", rows)
    conn.execute(
        "create table customers(customer_id integer, first_name varchar, last_name varchar, email varchar, "
        "region varchar, plan varchar, signup_date date)"
    )
    people = [
        (1, "Ada", "Lovelace", "ada@example.com", "west", "pro", date(2024, 1, 5)),
        (2, "Alan", "Turing", "alan@example.com", "east", "free", date(2024, 2, 5)),
        (3, "Grace", "Hopper", "grace@example.com", "west", "enterprise", date(2024, 3, 5)),
        (4, "Linus", "Torvalds", "linus@example.com", "east", "pro", date(2024, 4, 5)),
        (5, "Barbara", "Liskov", "barbara@example.com", "west", "free", date(2024, 5, 5)),
        (6, "Edsger", "Dijkstra", "edsger@example.com", "east", "pro", date(2024, 6, 5)),
        (7, "Donald", "Knuth", "donald@example.com", "west", "pro", date(2024, 7, 5)),
    ]
    conn.executemany("insert into customers values (?, ?, ?, ?, ?, ?, ?)", people)
    conn.close()


@pytest.fixture
def db_path(tmp_path):
    p = tmp_path / "test.duckdb"
    seed(p)
    return str(p)


def make_client(db_path, **settings):
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(db_path=db_path, **settings)
    app.dependency_overrides[get_today] = lambda: date(2025, 6, 1)
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def client(db_path):
    return make_client(db_path)


@pytest.fixture
def factory(db_path):
    """Build more clients over the same database (new app instance each time)."""
    return lambda **kw: make_client(db_path, **kw)
