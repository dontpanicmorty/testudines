def daily_total(connect, day: str) -> float:
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(amount) FROM orders WHERE order_date = %(day)s", {"day": day})
            row = cur.fetchone()
        return 0.0 if row is None or row[0] is None else float(row[0])
    finally:
        conn.close()
