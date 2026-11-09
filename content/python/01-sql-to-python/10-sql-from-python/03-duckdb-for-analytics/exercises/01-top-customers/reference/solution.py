import duckdb


def top_customers(data_dir, n: int) -> list[tuple[int, float]]:
    """Top n customers by non-cancelled revenue using DuckDB."""
    con = duckdb.connect()
    sql = """
        SELECT o.customer_id, ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
        FROM read_csv_auto(?) o JOIN read_csv_auto(?) i USING (order_id)
        WHERE o.status <> 'cancelled'
        GROUP BY o.customer_id
        ORDER BY revenue DESC, o.customer_id
        LIMIT ?
    """
    rows = con.execute(sql, [f"{data_dir}/orders.csv", f"{data_dir}/order_items.csv", n]).fetchall()
    return [(int(c), float(r)) for c, r in rows]
