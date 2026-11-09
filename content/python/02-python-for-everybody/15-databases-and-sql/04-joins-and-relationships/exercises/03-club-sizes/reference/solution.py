def club_sizes(conn):
    sql = """
        SELECT club.name, COUNT(membership.member_id) AS n
        FROM club
        LEFT JOIN membership ON membership.club_id = club.id
        GROUP BY club.id
        ORDER BY n DESC, club.name
    """
    return conn.execute(sql).fetchall()
