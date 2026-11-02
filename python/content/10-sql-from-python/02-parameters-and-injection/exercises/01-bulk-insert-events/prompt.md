The table `events(event_id TEXT PRIMARY KEY, user_id INTEGER, kind TEXT)` already exists. Write `insert_events(conn, events)` that bulk-inserts a list of dicts with those three keys and returns the number of rows **actually inserted**. Events whose `event_id` already exists must be skipped without error, so the same batch can be loaded twice. The data may contain quotes, so use parameters.

```python
batch = [{"event_id": "e1", "user_id": 1, "kind": "login"}]
insert_events(conn, batch)   # 1
insert_events(conn, batch)   # 0
```
