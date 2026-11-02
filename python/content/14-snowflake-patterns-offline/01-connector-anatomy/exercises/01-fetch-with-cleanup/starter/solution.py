def fetch_all(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur.fetchall()


def scalar(conn, sql, params=None, default=None):
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur.fetchone()[0]
