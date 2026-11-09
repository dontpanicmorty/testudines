import sqlite3


def search_products(conn: sqlite3.Connection, category=None, min_price=None,
                    sort_by: str = "name", direction: str = "asc") -> list[dict]:
    """Build a safe, dynamic query. See prompt.md."""
    raise NotImplementedError
