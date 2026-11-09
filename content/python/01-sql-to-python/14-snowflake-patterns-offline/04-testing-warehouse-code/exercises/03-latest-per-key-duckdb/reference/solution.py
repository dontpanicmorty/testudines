"""Logic you can verify on an in-memory DuckDB."""
import re


def _ident(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name or ""):
        raise ValueError(f"unsafe identifier: {name!r}")
    return name


def latest_per_key(con, table: str, key: str, ts_col: str) -> list[dict]:
    table, key, ts_col = _ident(table), _ident(key), _ident(ts_col)
    sql = (
        f"SELECT * FROM {table} "
        f"QUALIFY ROW_NUMBER() OVER (PARTITION BY {key} ORDER BY {ts_col} DESC) = 1 "
        f"ORDER BY {key}"
    )
    cur = con.execute(sql)
    names = [d[0] for d in cur.description]
    return [dict(zip(names, row)) for row in cur.fetchall()]
