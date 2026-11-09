import pytest


def days(body):
    return [(r["day"], r["region"]) for r in body["items"]]


def test_default_listing_ordered_and_shaped(client):
    body = client.get("/revenue/daily").json()
    assert body["total"] == 10 and body["page"] == 1 and body["page_size"] == 20
    assert body["has_next"] is False
    assert days(body)[:3] == [("2025-01-01", "east"), ("2025-01-01", "west"), ("2025-01-02", "east")]
    assert set(body["items"][0]) == {"day", "region", "orders", "revenue"}


def test_revenue_rounded_to_two_places(client):
    first = client.get("/revenue/daily").json()["items"][0]
    assert first["revenue"] == 100.0 or first["revenue"] == 100.01   # 100.005 rounded; accept either rounding mode
    assert len(str(first["revenue"]).split(".")[1]) <= 2


def test_date_range_is_inclusive(client):
    body = client.get("/revenue/daily?start=2025-01-02&end=2025-01-03").json()
    assert body["total"] == 4
    assert {d for d, _ in days(body)} == {"2025-01-02", "2025-01-03"}


def test_region_filter(client):
    body = client.get("/revenue/daily?region=west").json()
    assert body["total"] == 5 and {r for _, r in days(body)} == {"west"}


def test_unknown_region_is_empty_not_error(client):
    body = client.get("/revenue/daily?region=mars").json()
    assert body["items"] == [] and body["total"] == 0 and body["has_next"] is False


def test_filters_combine(client):
    body = client.get("/revenue/daily?region=east&start=2025-01-04").json()
    assert days(body) == [("2025-01-04", "east"), ("2025-01-05", "east")]


def test_start_after_end_is_422(client):
    r = client.get("/revenue/daily?start=2025-02-01&end=2025-01-01")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"
    assert "query.start" in r.json()["error"]["fields"]


@pytest.mark.parametrize("qs", ["start=yesterday", "end=2025-13-01", "page=0", "page_size=0", "page=x"])
def test_bad_parameters_are_422(client, qs):
    r = client.get(f"/revenue/daily?{qs}")
    assert r.status_code == 422, qs
    assert r.json()["error"]["code"] == "validation_error"


def test_pagination_walk_covers_everything_once(client):
    seen, page = [], 1
    while True:
        body = client.get(f"/revenue/daily?page={page}&page_size=3").json()
        seen += days(body)
        if not body["has_next"]:
            break
        page += 1
    assert page == 4
    assert len(seen) == 10 and len(set(seen)) == 10
    assert seen == sorted(seen)


def test_exact_last_page_has_no_next(client):
    body = client.get("/revenue/daily?page=2&page_size=5").json()
    assert len(body["items"]) == 5 and body["has_next"] is False


def test_page_beyond_end_is_empty(client):
    body = client.get("/revenue/daily?page=99").json()
    assert body["items"] == [] and body["total"] == 10


def test_page_size_above_max_is_422_naming_field(client):
    r = client.get("/revenue/daily?page_size=101")
    assert r.status_code == 422
    assert r.json()["error"]["fields"] == ["query.page_size"]


def test_default_and_max_page_size_come_from_settings(factory):
    c = factory(default_page_size=2, max_page_size=4)
    assert len(c.get("/revenue/daily").json()["items"]) == 2
    assert c.get("/revenue/daily?page_size=4").status_code == 200
    assert c.get("/revenue/daily?page_size=5").status_code == 422


def test_day_detail(client):
    body = client.get("/revenue/daily/2025-01-02").json()
    assert body["day"] == "2025-01-02"
    assert [r["region"] for r in body["regions"]] == ["east", "west"]
    assert body["orders"] == sum(r["orders"] for r in body["regions"]) == 2 + 3
    assert body["revenue"] == pytest.approx(sum(r["revenue"] for r in body["regions"]), abs=0.011)


def test_day_detail_missing_is_404_envelope(client):
    r = client.get("/revenue/daily/2030-01-01")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


def test_day_detail_bad_date_422(client):
    assert client.get("/revenue/daily/not-a-date").status_code == 422


def test_reads_are_repeatable_and_do_not_change_data(client):
    a = client.get("/revenue/daily?page_size=100").json()
    b = client.get("/revenue/daily?page_size=100").json()
    assert a == b
