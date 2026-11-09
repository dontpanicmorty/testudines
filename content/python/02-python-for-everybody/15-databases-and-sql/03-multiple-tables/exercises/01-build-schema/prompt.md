Write `create_schema(conn)`. It creates two tables if they do not already exist:

- `author` with columns `id` (automatically numbered primary key) and `name` (text, no two authors may share a name);
- `book` with columns `id` (automatically numbered primary key), `title` (text) and `author_id` (integer).

It must be safe to call twice.
