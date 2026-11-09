+++
id = "everybody.databases-and-sql.joins-and-relationships"
title = "Joins and many-to-many"
minutes = 30
+++

# Joins and many-to-many

Splitting data into tables saves space and keeps it consistent. But a report needs the pieces back together: book titles *with* their author names. That is the job of `JOIN`.

## JOIN reconnects tables

Take these two tables, with `book.author_id` pointing at `author.id`:

```python
import sqlite3
conn = sqlite3.connect(":memory:")
conn.executescript("""
    CREATE TABLE author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
    CREATE TABLE book (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author_id INTEGER);
    INSERT INTO author (name) VALUES ('Aldo Marsh'), ('Wren Okafor');
    INSERT INTO book (title, author_id) VALUES
        ('Tide Tables', 1), ('Fen Atlas', 1), ('Reed Songs', 2);
""")
```

(`executescript` runs several commands at once. It takes no `?` parameters, so use it only for fixed setup text.)

```python
sql = """
    SELECT book.title, author.name
    FROM book
    JOIN author ON book.author_id = author.id
    ORDER BY book.title
"""
for row in conn.execute(sql):
    print(row)
```

This prints:

```
('Fen Atlas', 'Aldo Marsh')
('Reed Songs', 'Wren Okafor')
('Tide Tables', 'Aldo Marsh')
```

Read it aloud: take each book, find the author whose `id` equals the book's `author_id`, and glue the two rows together. The `ON` clause is the matching rule. Writing `table.column` removes any doubt about which table a column comes from.

## LEFT JOIN keeps the lonely rows

A plain `JOIN` drops rows with no match. If an author has written no books, they vanish from the result. `LEFT JOIN` keeps every row from the left table and fills the missing side with `None`:

```python
conn.execute("INSERT INTO author (name) VALUES ('Ivy Chen')")
sql = """
    SELECT author.name, COUNT(book.id)
    FROM author
    LEFT JOIN book ON book.author_id = author.id
    GROUP BY author.id
    ORDER BY author.name
"""
print(conn.execute(sql).fetchall())
# [('Aldo Marsh', 2), ('Ivy Chen', 0), ('Wren Okafor', 1)]
```

`COUNT(book.id)` counts only real matches, so Ivy gets 0.

## Many-to-many relationships

A book has one author in our model. But a **member** can join many **clubs**, and a club has many members. That is a **many-to-many** relationship, and one extra column cannot hold it. The answer is a third table, called a **junction table**, with one row per pairing:

```
member               membership                 club
+----+------+        +-----------+---------+    +----+----------+
| id | name |<-------| member_id | club_id |--->| id | name     |
+----+------+        +-----------+---------+    +----+----------+
```

```python
conn.executescript("""
    CREATE TABLE member (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
    CREATE TABLE club   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
    CREATE TABLE membership (
        member_id INTEGER,
        club_id   INTEGER,
        UNIQUE (member_id, club_id)
    );
""")
```

The `UNIQUE (member_id, club_id)` constraint stops anyone joining the same club twice.

To list one member's clubs, join through the middle table:

```python
sql = """
    SELECT club.name
    FROM member
    JOIN membership ON membership.member_id = member.id
    JOIN club ON club.id = membership.club_id
    WHERE member.name = ?
    ORDER BY club.name
"""
conn.execute(sql, ("Ines",)).fetchall()
```

Chain as many joins as you need, one `JOIN ... ON ...` per table.

## Debugging joins

- **Too many rows?** You probably forgot the `ON` condition or matched the wrong columns. Run `SELECT COUNT(*)` on each table and think about what the join should produce.
- **Missing rows?** A plain `JOIN` drops unmatched rows. Try `LEFT JOIN`.
- **Duplicates?** One row on the left matched several on the right. That is correct behaviour, so use `COUNT(DISTINCT ...)` or `GROUP BY` if you wanted one line per left row.
- **"ambiguous column name" error?** Two tables share the column name. Write `table.column`.

When in doubt, shrink the problem: select `*` from the join with a `LIMIT 5` and look at the raw rows.

## Common mistakes

- Joining on the wrong columns, such as `book.id = author.id`.
- Using `JOIN` where `LEFT JOIN` is needed to keep rows with no match.
- Forgetting the junction table and trying to store a list in one column.
- Not making the pair unique in a junction table.
