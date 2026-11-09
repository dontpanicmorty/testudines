from pathlib import Path

import duckdb


def write_parquet(rows: list[dict], path) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("CREATE TABLE t (sku VARCHAR, qty BIGINT, price DOUBLE)")
    if rows:
        con.executemany("INSERT INTO t VALUES (?, ?, ?)", [[r["sku"], r["qty"], r["price"]] for r in rows])
    con.execute(f"COPY t TO '{path}' (FORMAT PARQUET)")
    return len(rows)


def read_parquet_rows(path, min_qty: int = 0) -> list[dict]:
    con = duckdb.connect()
    cur = con.execute(
        "SELECT sku, qty, price FROM read_parquet(?) WHERE qty >= ? ORDER BY sku",
        [str(path), min_qty],
    )
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]
