"""Idempotent loading into sqlite, plus watermark and quarantine bookkeeping."""
import sqlite3
from pathlib import Path

SCHEMA = """
create table if not exists daily_revenue (
    day text not null,
    region text not null,
    orders integer not null,
    revenue real not null,
    primary key (day, region)
);
create table if not exists quarantine (
    row_key text primary key,
    source text not null,
    reason text not null,
    raw text not null
);
create table if not exists pipeline_state (
    key text primary key,
    value text not null
);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    """Open the database and make sure the tables exist (safe to call repeatedly)."""
    raise NotImplementedError


def load_daily_revenue(conn: sqlite3.Connection, rows: list[dict], replace_all: bool = False) -> int:
    """Load rows idempotently and atomically; return len(rows)."""
    raise NotImplementedError


def save_quarantine(conn: sqlite3.Connection, bad_rows: list[dict]) -> int:
    """Store quarantined rows so that saving the same rows twice does not duplicate them."""
    raise NotImplementedError


def get_watermark(conn: sqlite3.Connection) -> str | None:
    raise NotImplementedError


def set_watermark(conn: sqlite3.Connection, day: str) -> None:
    raise NotImplementedError
