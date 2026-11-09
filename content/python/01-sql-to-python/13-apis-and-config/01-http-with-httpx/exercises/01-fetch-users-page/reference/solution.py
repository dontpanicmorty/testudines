import httpx


def fetch_users_page(client: httpx.Client, page: int) -> list[dict]:
    resp = client.get("/users", params={"page": page})
    resp.raise_for_status()
    return resp.json()["results"]
