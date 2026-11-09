An events API responds to `GET /events` with `{"data": [...], "next_cursor": "<token>" | null}`. Pass the token back as the `cursor` query parameter to get the next page. The first request has no `cursor`.

Write the **generator** `iter_events(client)` that yields every event across all pages. It must be lazy: requesting the first event must not fetch page two. Raise for bad statuses.

```python
list(iter_events(client))          # every event, in order
next(iter(iter_events(client)))    # only one request is made
```
