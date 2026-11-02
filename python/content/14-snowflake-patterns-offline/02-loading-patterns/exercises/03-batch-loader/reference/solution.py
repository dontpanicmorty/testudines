from itertools import islice


def load_rows(conn, table, columns, rows, batch_size=1000):
    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    total = 0
    cur = conn.cursor()
    try:
        it = iter(rows)
        while True:
            batch = [tuple(r[c] for c in columns) for r in islice(it, batch_size)]
            if not batch:
                break
            cur.executemany(sql, batch)
            total += len(batch)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
    return total
