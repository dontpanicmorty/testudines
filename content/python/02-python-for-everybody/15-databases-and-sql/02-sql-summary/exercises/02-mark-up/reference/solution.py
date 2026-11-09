def discount_old(conn, before_year, percent):
    cur = conn.execute(
        "UPDATE book SET price = price * (100 - ?) / 100 WHERE year < ?",
        (percent, before_year),
    )
    conn.commit()
    return cur.rowcount
