import json
import os
from pathlib import Path

from solution import active_names, make_mock_client

DATA = Path(os.environ["DOJO_DATA"])


def _expected_active():
    names = []
    n = 1
    while (DATA / f"api_users_page{n}.json").exists():
        body = json.loads((DATA / f"api_users_page{n}.json").read_text())
        names += [u["name"] for u in body["results"] if u["active"]]
        n += 1
    return names


def test_serves_page_file():
    client = make_mock_client(DATA)
    resp = client.get("/users", params={"page": 2})
    assert resp.status_code == 200
    assert resp.json() == json.loads((DATA / "api_users_page2.json").read_text())


def test_missing_page_is_404():
    client = make_mock_client(DATA)
    resp = client.get("/users", params={"page": 99})
    assert resp.status_code == 404
    assert resp.json() == {"error": "not found"}


def test_unknown_path_is_404():
    assert make_mock_client(DATA).get("/other").status_code == 404


def test_active_names_walks_all_pages():
    got = active_names(make_mock_client(DATA))
    assert got == _expected_active()
    assert len(got) > 0


def test_works_with_custom_directory(tmp_path):
    (tmp_path / "api_users_page1.json").write_text(
        json.dumps({"page": 1, "results": [{"id": 1, "name": "A", "active": True}], "next": 2})
    )
    (tmp_path / "api_users_page2.json").write_text(
        json.dumps({"page": 2, "results": [{"id": 2, "name": "B", "active": False},
                                           {"id": 3, "name": "C", "active": True}], "next": None})
    )
    assert active_names(make_mock_client(tmp_path)) == ["A", "C"]
