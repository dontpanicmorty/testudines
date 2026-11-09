"""SQL builders whose output is easy to assert on."""
import re

_IDENT = r"[A-Za-z_][A-Za-z0-9_$]*"


def _check(name: str, pattern: str = _IDENT) -> str:
    if not isinstance(name, str) or not re.fullmatch(pattern, name):
        raise ValueError(f"unsafe identifier: {name!r}")
    return name


def build_select(table: str, columns: list[str], filters: dict | None = None) -> tuple[str, dict]:
    if not columns:
        raise ValueError("columns must not be empty")
    _check(table, rf"{_IDENT}(\.{_IDENT})?")
    cols = ", ".join(_check(c) for c in columns)
    filters = dict(filters or {})
    sql = f"SELECT {cols} FROM {table}"
    if filters:
        where = " AND ".join(f"{_check(k)} = %({k})s" for k in filters)
        sql += f" WHERE {where}"
    return sql, filters
