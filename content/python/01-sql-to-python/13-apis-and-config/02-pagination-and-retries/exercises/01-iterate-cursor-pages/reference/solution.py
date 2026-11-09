from collections.abc import Iterator

import httpx


def iter_events(client: httpx.Client) -> Iterator[dict]:
    cursor: str | None = None
    while True:
        params = {"cursor": cursor} if cursor is not None else {}
        resp = client.get("/events", params=params)
        resp.raise_for_status()
        body = resp.json()
        yield from body["data"]
        cursor = body["next_cursor"]
        if cursor is None:
            return
