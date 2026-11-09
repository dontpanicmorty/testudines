def clubs_of(conn, member_name):
    sql = """
        SELECT club.name
        FROM member
        JOIN membership ON membership.member_id = member.id
        JOIN club ON club.id = membership.club_id
        WHERE member.name = ?
        ORDER BY club.name
    """
    return [r[0] for r in conn.execute(sql, (member_name,))]
