from collections.abc import Iterator

import httpx


def iter_events(client: httpx.Client) -> Iterator[dict]:
    # TODO: loop over pages using next_cursor; yield each event lazily
    raise NotImplementedError
