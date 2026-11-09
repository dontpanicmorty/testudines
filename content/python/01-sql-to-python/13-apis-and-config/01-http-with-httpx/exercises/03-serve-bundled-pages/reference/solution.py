"""Build a fake users API from bundled JSON files and walk its pages."""
import json
from pathlib import Path

import httpx


def make_mock_client(data_dir: Path) -> httpx.Client:
    data_dir = Path(data_dir)

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path != "/users":
            return httpx.Response(404, json={"error": "not found"})
        page = int(request.url.params.get("page", "1"))
        path = data_dir / f"api_users_page{page}.json"
        if not path.exists():
            return httpx.Response(404, json={"error": "not found"})
        return httpx.Response(200, json=json.loads(path.read_text()))

    return httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.example.test")


def active_names(client: httpx.Client) -> list[str]:
    names: list[str] = []
    page: int | None = 1
    while page is not None:
        resp = client.get("/users", params={"page": page})
        resp.raise_for_status()
        body = resp.json()
        names.extend(u["name"] for u in body["results"] if u["active"])
        page = body["next"]
    return names
