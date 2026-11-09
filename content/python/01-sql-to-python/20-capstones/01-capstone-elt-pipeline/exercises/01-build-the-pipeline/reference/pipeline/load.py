"""Idempotent loading into sqlite, plus watermark and quarantine bookkeeping."""
import hashlib
import json
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
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    return conn


def load_daily_revenue(conn: sqlite3.Connection, rows: list[dict], replace_all: bool = False) -> int:
    with conn:
        if replace_all:
            conn.execute("delete from daily_revenue")
        else:
            days = sorted({r["day"] for r in rows})
            conn.executemany("delete from daily_revenue where day = ?", [(d,) for d in days])
        conn.executemany(
            "insert into daily_revenue (day, region, orders, revenue) values (:day, :region, :orders, :revenue)",
            rows,
        )
    return len(rows)


def save_quarantine(conn: sqlite3.Connection, bad_rows: list[dict]) -> int:
    records = []
    for b in bad_rows:
        raw = json.dumps(b["raw"], sort_keys=True)
        key = hashlib.sha1(json.dumps([b["source"], b["raw"]], sort_keys=True).encode()).hexdigest()
        records.append((key, b["source"], b["reason"], raw))
    with conn:
        conn.executemany("insert or replace into quarantine values (?, ?, ?, ?)", records)
    return len(records)


def get_watermark(conn: sqlite3.Connection) -> str | None:
    row = conn.execute("select value from pipeline_state where key = 'watermark'").fetchone()
    return row[0] if row else None


def set_watermark(conn: sqlite3.Connection, day: str) -> None:
    with conn:
        conn.execute("insert or replace into pipeline_state (key, value) values ('watermark', ?)", (day,))
