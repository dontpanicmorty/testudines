def rows_as_dicts(cur):
    if cur.description is None:
        return []
    names = [col[0].lower() for col in cur.description]
    return [dict(zip(names, row)) for row in cur.fetchall()]
