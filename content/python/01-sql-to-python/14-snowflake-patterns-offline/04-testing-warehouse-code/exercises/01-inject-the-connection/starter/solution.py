def open_real_connection():
    raise RuntimeError("no warehouse available in this environment")


def daily_total(day: str) -> float:
    conn = open_real_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT SUM(amount) FROM orders WHERE order_date = %(day)s", {"day": day})
        row = cur.fetchone()
    return float(row[0])
