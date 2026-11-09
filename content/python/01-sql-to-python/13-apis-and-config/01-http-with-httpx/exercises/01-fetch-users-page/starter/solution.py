import httpx


def fetch_users_page(client: httpx.Client, page: int) -> list[dict]:
    # TODO: GET /users with ?page=<page>, raise on bad status, return the "results" list
    raise NotImplementedError
