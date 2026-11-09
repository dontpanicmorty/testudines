+++
id = "everybody.databases-and-sql.first-database"
title = "Your first database"
minutes = 30
+++

# Your first database

Files are fine for small jobs. But when you have thousands of rows, want to look things up fast, or need several programs to share the same data safely, a **database** is the better tool.

## What a database is

A database is a file (or a service) built for storing and finding organized data. It keeps data on disk, so it survives when your program ends, and it can answer questions about the data quickly without reading everything.

The kind we use here is a **relational** database. It stores data in **tables**. You can picture a table as a spreadsheet:

| id | station | bikes |
|----|---------|-------|
| 1  | Mill Lane | 4 |
| 2  | Quay Street | 0 |
| 3  | Hill Top | 9 |

- A **table** holds one kind of thing (stations).
- A **row** (also called a record) is one thing: one station.
- A **column** (also called a field) is one fact about every row: the station name, the bike count.
- A **relation** is a link between tables, which you meet in the next lessons.

Programs talk to a database in a language called **SQL** (Structured Query Language, often said "sequel").

## SQLite

Python includes **SQLite**, a complete database that lives in a single file and needs no setup. The `sqlite3` module is how you use it. The same ideas carry over to big database systems.

## Browser tools

Programs are not the only way in. A **database browser** is an app that opens a database file and lets you see its tables, run SQL and edit rows with the mouse. It is useful for checking what your program actually stored. This course does not need one, because you can always inspect data from Python.

## Connect, cursor, execute, commit

```python
import sqlite3

conn = sqlite3.connect("bikes.db")     # opens the file, creating it if needed
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS station (name TEXT, bikes INTEGER)")
cur.execute("INSERT INTO station (name, bikes) VALUES ('Mill Lane', 4)")
conn.commit()
conn.close()
```

What each step does:

- `sqlite3.connect(path)` returns a **connection**, your open line to the file. Use `":memory:"` as the path for a throwaway database that lives only in RAM, which is perfect for tests.
- `conn.cursor()` gives you a **cursor**, the object that sends SQL commands and holds results.
- `cur.execute(sql)` sends one SQL command.
- `conn.commit()` makes your changes permanent. Until you commit, inserts and updates are only tentative and are lost if the program stops.
- `conn.close()` finishes.

## Reading rows

```python
conn = sqlite3.connect("bikes.db")
cur = conn.cursor()
cur.execute("SELECT name, bikes FROM station")
for row in cur:
    print(row)         # ('Mill Lane', 4)
```

Each row arrives as a **tuple** in the column order you asked for. `cur.fetchone()` returns one row (or `None`), and `cur.fetchall()` returns a list of all rows.

## Parameters with ?

Never build SQL by gluing user text into a string:

```python
name = "O'Neil Quay"
cur.execute(f"SELECT bikes FROM station WHERE name = '{name}'")   # DON'T
```

The apostrophe breaks the command, and a malicious value could even rewrite it (an attack called **SQL injection**). Instead, put a `?` placeholder in the SQL and hand the values separately, as a tuple:

```python
cur.execute("SELECT bikes FROM station WHERE name = ?", (name,))
cur.execute("INSERT INTO station (name, bikes) VALUES (?, ?)", ("Hill Top", 9))
```

The database inserts the values safely, with quoting handled for you. Note the comma in `(name,)`: a one-item tuple needs it.

To insert many rows at once, use `executemany`:

```python
rows = [("Quay Street", 0), ("Park Gate", 6)]
cur.executemany("INSERT INTO station (name, bikes) VALUES (?, ?)", rows)
conn.commit()
```

## Data types

SQLite columns commonly use `TEXT`, `INTEGER` and `REAL` (decimal numbers). Python converts automatically: `str`, `int`, `float`, and `None` for a missing value (SQL `NULL`).

## Common mistakes

- Forgetting `conn.commit()` and wondering why the data vanished.
- Building SQL with f-strings instead of `?` placeholders.
- Passing a single value instead of a tuple: `(name)` is just `name`, but `(name,)` is a tuple.
- Running `CREATE TABLE` twice. Add `IF NOT EXISTS`.
- Leaving connections open; call `close()` when you are done.
