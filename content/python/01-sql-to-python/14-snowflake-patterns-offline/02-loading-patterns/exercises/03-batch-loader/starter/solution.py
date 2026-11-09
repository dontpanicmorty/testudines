def load_rows(conn, table, columns, rows, batch_size=1000):
    cur = conn.cursor()
    for row in rows:
        cur.execute(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})",
            tuple(row[c] for c in columns),
        )
        conn.commit()
    return 0
