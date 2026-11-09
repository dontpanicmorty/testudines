def load_partition(conn, load_date, rows):
    with conn:
        conn.execute("delete from fact_orders where load_date = ?", (load_date,))
        conn.executemany(
            "insert into fact_orders (load_date, order_id, amount) values (?, ?, ?)",
            [(load_date, order_id, amount) for order_id, amount in rows],
        )
