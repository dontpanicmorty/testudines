+++
id = "everybody.databases-and-sql.sql-summary"
title = "The five SQL commands"
minutes = 30
+++

# The five SQL commands

You can do a surprising amount with five commands. This lesson is your quick reference, with each command run from Python. We will use a small table of books:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE book (title TEXT, year INTEGER, price REAL)")
```

`CREATE TABLE` names the table and lists each column with a type. That is command number one.

## INSERT: add a row

```python
conn.execute("INSERT INTO book (title, year, price) VALUES (?, ?, ?)",
             ("Tide Tables", 1999, 12.5))
conn.execute("INSERT INTO book (title, year, price) VALUES (?, ?, ?)",
             ("Moss and Stone", 2011, 8.0))
conn.execute("INSERT INTO book (title, year, price) VALUES (?, ?, ?)",
             ("Reed Songs", 2003, 15.0))
conn.commit()
```

The column list in parentheses says which columns you fill. The `VALUES` are matched up in the same order.

## SELECT: read rows

```python
for row in conn.execute("SELECT title, price FROM book"):
    print(row)
```

`SELECT` lists the columns you want, and `FROM` says the table. Use `*` for every column, although naming columns is clearer.

### WHERE filters the rows

```python
cur = conn.execute("SELECT title FROM book WHERE year > ?", (2000,))
print(cur.fetchall())     # [('Moss and Stone',), ('Reed Songs',)]
```

`WHERE` keeps only rows where the condition is true. Combine conditions with `AND` and `OR`, and compare with `=`, `<>` (not equal), `<`, `>`, `<=`, `>=`. Notice SQL uses a single `=` to compare.

For text matching use `LIKE`, where `%` stands for any run of characters:

```python
conn.execute("SELECT title FROM book WHERE title LIKE ?", ("M%",))
```

### ORDER BY sorts

```python
conn.execute("SELECT title, price FROM book ORDER BY price DESC")
```

`ORDER BY` sorts the results; add `DESC` for largest first. Without `ORDER BY`, the order is **not guaranteed**. To keep only the first few, add `LIMIT`:

```python
conn.execute("SELECT title FROM book ORDER BY year LIMIT 2")
```

## UPDATE: change rows

```python
cur = conn.execute("UPDATE book SET price = price * 1.1 WHERE year < ?", (2005,))
print(cur.rowcount)    # how many rows changed
conn.commit()
```

`SET` names the new value. The `WHERE` part is crucial: **without it, every row changes**. After any write, `cur.rowcount` tells you how many rows were affected, which is a good sanity check.

## DELETE: remove rows

```python
cur = conn.execute("DELETE FROM book WHERE price < ?", (9,))
conn.commit()
```

Again, always include a `WHERE`, unless you truly mean to empty the table.

## Counting and totals

SQL can do arithmetic over many rows with **aggregate** functions:

```python
conn.execute("SELECT COUNT(*), AVG(price), MAX(year) FROM book").fetchone()
```

`COUNT(*)` counts rows, `SUM`, `AVG`, `MIN` and `MAX` work on a column. Add `GROUP BY` to get one result per category:

```python
conn.execute("SELECT year / 10 * 10 AS decade, COUNT(*) FROM book GROUP BY decade")
```

## Reading the results

- `cur.fetchone()` is one row or `None`.
- `cur.fetchall()` is a list of tuples.
- Looping over `cur` goes row by row.
- `conn.row_factory = sqlite3.Row` lets you read columns by name, like `row["title"]`.

## Debugging tip

Most SQL bugs are visible by printing. Run the `SELECT` on its own and look at the rows. If an UPDATE or DELETE touched the wrong rows, check its `rowcount` and rerun the same `WHERE` as a `SELECT` first to preview what it will hit.

## Common mistakes

- Forgetting `WHERE` on `UPDATE` or `DELETE`.
- Using `==` instead of `=` in SQL.
- Assuming rows come back in insertion order without `ORDER BY`.
- Forgetting to commit after a write.
- Putting quotes around a `?` placeholder: write `?`, not `'?'`.
