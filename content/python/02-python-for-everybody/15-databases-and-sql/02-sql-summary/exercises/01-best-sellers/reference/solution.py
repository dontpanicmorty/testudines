def priciest(conn, n):
    cur = conn.execute("SELECT title FROM book ORDER BY price DESC, title LIMIT ?", (n,))
    return [row[0] for row in cur]
