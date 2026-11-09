"""Runs and grades SQL answers with DuckDB, entirely on this computer.

Every run and check uses a fresh in-memory database seeded from the exercise's schema.sql, so an answer
can't be affected by an earlier one. A check runs the learner's SQL and the reference solution and
compares their results the way SQL Dojo always has: each row's values are compared as a set (column
order doesn't matter) and the rows are compared as a set (row order doesn't matter, unless the prompt
asks for an order the reference shows — order is never graded).

DuckDB runs inside the app, so every query is kept small (DuckDB's defaults are every CPU core and 80% of
the computer's memory, which a runaway join would use):
- memory_limit_mb(): 256 MB, or less on a computer with under 4 GB. The exercises' tables are tiny; a
  query that needs more is stopped with an "out of memory" message;
- 2 threads, and at most QUERY_SECONDS seconds per query;
- at most MAX_ROWS rows of a result are kept;
- no file, network or extension access: exercises only use the tables their schema.sql creates.
"""
from __future__ import annotations

import datetime as _dt
import decimal
import json
import re
import threading
from dataclasses import dataclass, field

import duckdb
import psutil

SAMPLE_ROWS = 30         # rows shown per sample table
MAX_ROWS = 100_000       # rows of a result kept; no exercise expects more
QUERY_SECONDS = 20       # longest a query may run


def memory_limit_mb() -> int:
    total_mb = psutil.virtual_memory().total // (1024 * 1024)
    return int(max(64, min(256, total_mb // 16)))


CONFIG = {"memory_limit": f"{memory_limit_mb()}MB", "threads": 2, "enable_external_access": False,
          "autoinstall_known_extensions": False, "autoload_known_extensions": False}


@dataclass
class Result:
    columns: list[str] = field(default_factory=list)
    rows: list[tuple] = field(default_factory=list)
    error: str = ""
    truncated: bool = False  # the query returned more than MAX_ROWS rows; only the first MAX_ROWS are kept


def _connect(schema: str) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(":memory:", config=CONFIG)
    for statement in con.extract_statements(schema):
        con.execute(statement.query)
    return con


def _error(exc: Exception) -> str:
    if isinstance(exc, duckdb.InterruptException):
        return f"The query was stopped after {QUERY_SECONDS} seconds. Is a join or recursion running away?"
    if isinstance(exc, duckdb.OutOfMemoryException):
        return ("The query needed more memory than an exercise ever should "
                f"({memory_limit_mb()} MB). Is a join multiplying rows?")
    return _first_line(exc)


def run(schema: str, sql: str) -> Result:
    """Run every statement of sql on a fresh copy of the tables; the result of the last one that returns rows."""
    try:
        con = _connect(schema)
    except duckdb.Error as exc:
        return Result(error=f"The exercise's tables couldn't be created: {_first_line(exc)}")
    out = Result()
    timer = threading.Timer(QUERY_SECONDS, con.interrupt)  # stops a query that runs too long
    timer.daemon = True
    timer.start()
    try:
        statements = con.extract_statements(sql)
        if not statements:
            return Result(error="Write a query first.")
        for statement in statements:
            rel = con.execute(statement.query)
            if rel.description:
                rows = rel.fetchmany(MAX_ROWS + 1)
                out = Result([d[0] for d in rel.description], rows[:MAX_ROWS], truncated=len(rows) > MAX_ROWS)
    except duckdb.Error as exc:
        return Result(error=_error(exc))
    finally:
        timer.cancel()
        con.close()
    return out


def _first_line(exc: Exception) -> str:
    return str(exc).strip().split("\n")[0]


def normalize(v) -> str:
    """One value as text, so values from either query compare the same way."""
    if v is None:
        return "␀NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (_dt.datetime, _dt.date, _dt.time)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return format(v.normalize(), "f") if v == v.to_integral_value() else str(v.normalize())
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, (list, dict, tuple)):
        return json.dumps(v, default=str, sort_keys=True)
    return str(v)


def signature(rows: list[tuple]) -> list[str]:
    """Rows as comparable text: values sorted within each row, then rows sorted."""
    return sorted(json.dumps(sorted(normalize(v) for v in row)) for row in rows)


def check(schema: str, solution: str, sql: str) -> dict:
    """{passed, result, expected_rows, error, message}: the learner's result and how it compares."""
    mine = run(schema, sql)
    if mine.error:
        return {"passed": False, "result": mine, "expected_rows": None, "error": mine.error,
                "message": f"SQL error: {mine.error}"}
    expected = run(schema, solution)
    if expected.error:
        return {"passed": False, "result": mine, "expected_rows": None, "error": expected.error,
                "message": f"The reference solution failed ({expected.error}); please report this exercise."}
    if mine.truncated:
        return {"passed": False, "result": mine, "expected_rows": len(expected.rows), "error": "",
                "message": f"Not quite — expected {len(expected.rows)} row(s), got more than {MAX_ROWS:,}. "
                           "Is a join multiplying rows?"}
    if signature(mine.rows) == signature(expected.rows):
        return {"passed": True, "result": mine, "expected_rows": len(expected.rows), "error": "",
                "message": f"✓ Correct! {len(expected.rows)} row(s) matched."}
    return {"passed": False, "result": mine, "expected_rows": len(expected.rows), "error": "",
            "message": f"Not quite — expected {len(expected.rows)} row(s), got {len(mine.rows)}. "
                       "Check column selection, filters, and row values."}


TABLE_NAME = re.compile(r"(?i)create\s+(?:or\s+replace\s+)?table\s+(?:if\s+not\s+exists\s+)?(\w+)")


def sample_tables(schema: str) -> list[dict]:
    """Each table the exercise creates, with up to SAMPLE_ROWS of its rows: [{name, columns, rows, total}]."""
    names = list(dict.fromkeys(TABLE_NAME.findall(schema)))
    out = []
    try:
        con = _connect(schema)
    except duckdb.Error:
        return out
    try:
        for name in names:
            rel = con.execute(f'select * from "{name}" limit {SAMPLE_ROWS}')
            cols = [d[0] for d in rel.description]
            rows = rel.fetchall()
            total = con.execute(f'select count(*) from "{name}"').fetchone()[0]
            out.append({"name": name, "columns": cols, "rows": rows, "total": total})
    finally:
        con.close()
    return out
