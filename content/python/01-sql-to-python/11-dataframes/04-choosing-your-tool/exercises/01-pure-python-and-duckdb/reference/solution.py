from collections import defaultdict

import duckdb


def top_python(orders: list[dict], items: list[dict], n: int) -> list[tuple[int, float]]:
    """Plain Python: dicts and loops."""
    owner = {o["order_id"]: o["customer_id"] for o in orders if o["status"] != "cancelled"}
    totals: dict[int, float] = defaultdict(float)
    for it in items:
        cust = owner.get(it["order_id"])
        if cust is not None:
            totals[cust] += it["quantity"] * it["unit_price"]
    ranked = sorted(((c, round(t, 2)) for c, t in totals.items()), key=lambda kv: (-kv[1], kv[0]))
    return [(int(c), float(t)) for c, t in ranked[:n]]


def top_duckdb(orders: list[dict], items: list[dict], n: int) -> list[tuple[int, float]]:
    """DuckDB: load the rows into in-memory tables and run one query."""
    con = duckdb.connect()
    con.execute("CREATE TABLE o (order_id BIGINT, customer_id BIGINT, status VARCHAR)")
    con.execute("CREATE TABLE i (order_id BIGINT, quantity BIGINT, unit_price DOUBLE)")
    if orders:
        con.executemany("INSERT INTO o VALUES (?, ?, ?)", [[r["order_id"], r["customer_id"], r["status"]] for r in orders])
    if items:
        con.executemany("INSERT INTO i VALUES (?, ?, ?)", [[r["order_id"], r["quantity"], r["unit_price"]] for r in items])
    rows = con.execute(
        """
        SELECT o.customer_id, ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
        FROM o JOIN i USING (order_id) WHERE o.status <> 'cancelled'
        GROUP BY 1 ORDER BY revenue DESC, 1 LIMIT ?
        """, [n]).fetchall()
    return [(int(c), float(r)) for c, r in rows]
