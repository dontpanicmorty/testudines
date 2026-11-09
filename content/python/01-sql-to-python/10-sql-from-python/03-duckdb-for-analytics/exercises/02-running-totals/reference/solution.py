import duckdb


def running_totals(entries: list[tuple[str, str, int]]) -> list[tuple[str, str, int, int]]:
    """Cumulative amount per account, in date order, via a window function."""
    con = duckdb.connect()
    con.execute("CREATE TABLE ledger (account VARCHAR, day VARCHAR, amount BIGINT)")
    if entries:
        con.executemany("INSERT INTO ledger VALUES (?, ?, ?)", [list(e) for e in entries])
    rows = con.execute(
        """
        SELECT account, day, amount,
               SUM(amount) OVER (PARTITION BY account ORDER BY day) AS running_total
        FROM ledger
        ORDER BY account, day
        """
    ).fetchall()
    return [(a, d, int(m), int(r)) for a, d, m, r in rows]
