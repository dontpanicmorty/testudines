import sqlite3


def transfer(conn: sqlite3.Connection, src: int, dst: int, amount: int) -> None:
    with conn:
        cur = conn.execute("UPDATE acct SET balance = balance - ? WHERE id = ?", (amount, src))
        if cur.rowcount == 0:
            raise ValueError(f"unknown account {src}")
        cur = conn.execute("UPDATE acct SET balance = balance + ? WHERE id = ?", (amount, dst))
        if cur.rowcount == 0:
            raise ValueError(f"unknown account {dst}")
        row = conn.execute("SELECT balance FROM acct WHERE id = ?", (src,)).fetchone()
        if row[0] < 0:
            raise ValueError("insufficient funds")
