import sqlite3

SORTABLE = {"product_id", "name", "category", "unit_price"}


def search_products(conn: sqlite3.Connection, category=None, min_price=None,
                    sort_by: str = "name", direction: str = "asc") -> list[dict]:
    if sort_by not in SORTABLE:
        raise ValueError(f"cannot sort by {sort_by!r}")
    if direction.lower() not in {"asc", "desc"}:
        raise ValueError("direction must be asc or desc")
    conditions: list[str] = []
    params: list = []
    if category is not None:
        conditions.append("category = ?")
        params.append(category)
    if min_price is not None:
        conditions.append("unit_price >= ?")
        params.append(min_price)
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = (f"SELECT product_id, name, category, unit_price FROM products {where} "
           f"ORDER BY {sort_by} {direction.upper()}, product_id")
    previous = conn.row_factory
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(sql, params)]
    finally:
        conn.row_factory = previous
