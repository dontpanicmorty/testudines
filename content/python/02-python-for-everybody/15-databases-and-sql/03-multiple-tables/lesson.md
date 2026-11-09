+++
id = "everybody.databases-and-sql.multiple-tables"
title = "Several tables and keys"
minutes = 30
+++

# Several tables and keys

Imagine storing every loan of a library like this, in one table:

| member | book | author |
|--------|------|--------|
| Ines | Tide Tables | Aldo Marsh |
| Omar | Tide Tables | Aldo Marsh |
| Ines | Reed Songs | Wren Okafor |

"Aldo Marsh" is typed out again and again. That wastes space, and worse, if you misspell it once, your data disagrees with itself. The fix is a golden rule of data modeling: **do not repeat string data**. Store each fact once, and point to it.

## Splitting into tables

Make one table for authors, one for books. Each book then stores a small number that points at its author.

```
author                    book
+----+-------------+      +----+--------------+-----------+
| id | name        |      | id | title        | author_id |
+----+-------------+      +----+--------------+-----------+
|  1 | Aldo Marsh  |<-----|  1 | Tide Tables  |     1     |
|  2 | Wren Okafor |<-----|  2 | Reed Songs   |     2     |
+----+-------------+      +----+--------------+-----------+
```

A sketch like this is a **data model diagram**. Each box is a table, each line is a link. The link from `book.author_id` to `author.id` is a relation.

## Primary keys

Each row needs an identity that never changes. This is the **primary key**. In SQLite the usual choice is an integer the database hands out automatically:

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS author (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS book (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        title     TEXT,
        author_id INTEGER
    )
""")
```

`INTEGER PRIMARY KEY AUTOINCREMENT` means: number rows 1, 2, 3 and so on for me, and never reuse a number. You leave `id` out of your `INSERT` and the database fills it in.

A column such as `book.author_id` that holds another table's primary key is called a **foreign key**.

## Logical keys and UNIQUE

The `id` is for the machine. The **logical key** is the real-world value you use to find a row, such as an author's name. Marking it `UNIQUE` does two things: the database refuses duplicates, and it builds an index so lookups by that column are fast.

```python
conn.execute("INSERT INTO author (name) VALUES (?)", ("Aldo Marsh",))
conn.execute("INSERT INTO author (name) VALUES (?)", ("Aldo Marsh",))
# sqlite3.IntegrityError: UNIQUE constraint failed: author.name
```

That rule is a **constraint**: a promise the database enforces for you. Constraints catch bugs early.

## INSERT OR IGNORE

Often you want "make sure this exists" without an error. `INSERT OR IGNORE` quietly skips the insert if a constraint would be broken:

```python
conn.execute("INSERT OR IGNORE INTO author (name) VALUES (?)", ("Aldo Marsh",))
```

## Get or create

This is the key pattern: given a name, give me its id, creating the row if needed.

```python
def author_id(conn, name):
    conn.execute("INSERT OR IGNORE INTO author (name) VALUES (?)", (name,))
    row = conn.execute("SELECT id FROM author WHERE name = ?", (name,)).fetchone()
    return row[0]
```

First ensure the row exists, then look up its id. It works whether the author is new or old.

## lastrowid

After an insert, `cur.lastrowid` is the primary key the database just assigned:

```python
cur = conn.execute("INSERT INTO book (title, author_id) VALUES (?, ?)", ("Tide Tables", 1))
print(cur.lastrowid)      # 1
```

Careful: after an `INSERT OR IGNORE` that was ignored, `lastrowid` is not reliable, so use the SELECT as above for lookups.

## Putting it together

```python
def add_book(conn, title, author):
    aid = author_id(conn, author)
    cur = conn.execute("INSERT INTO book (title, author_id) VALUES (?, ?)", (title, aid))
    conn.commit()
    return cur.lastrowid
```

Adding ten books by the same author stores their name once.

## Common mistakes

- Repeating text in many rows instead of storing it once and pointing to it.
- Inserting a value for an `AUTOINCREMENT` id by hand.
- Forgetting `UNIQUE` on the logical key, then getting duplicates and an unreliable lookup.
- Trusting `lastrowid` after an insert that was ignored.
- Forgetting to `commit` after the whole get-or-create sequence.
