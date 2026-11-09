from solution import activity


def test_example():
    msgs = [("A <a@mail.x.org>", "2026-01-02"), ("b@X.org", "2026-02-01")]
    assert activity(msgs) == {"by_org": [("x.org", 2)], "by_month": [("2026-01", 1), ("2026-02", 1)]}


def test_ordering():
    msgs = [
        ("a@zed.org", "2026-03-01"), ("b@alpha.com", "2026-03-02"),
        ("c@beta.net", "2026-01-05"), ("d@beta.net", "2026-01-09"),
    ]
    out = activity(msgs)
    assert out["by_org"] == [("beta.net", 2), ("alpha.com", 1), ("zed.org", 1)]
    assert out["by_month"] == [("2026-01", 2), ("2026-03", 2)]


def test_empty():
    assert activity([]) == {"by_org": [], "by_month": []}


def test_messy_senders_merge():
    msgs = [("  Ines <INES@Mail.Example.ORG> ", "2026-05-01"), ("ines@example.org", "2026-05-02")]
    assert activity(msgs)["by_org"] == [("example.org", 2)]
