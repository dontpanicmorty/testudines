def catalogue(conn):
    sql = """
        SELECT book.title, author.name
        FROM book JOIN author ON book.author_id = author.id
        ORDER BY book.title
    """
    return conn.execute(sql).fetchall()
