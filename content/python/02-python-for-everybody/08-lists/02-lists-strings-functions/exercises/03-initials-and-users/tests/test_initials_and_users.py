from solution import senders


def test_basic():
    lines = [
        "From: sam@example.org",
        "Subject: hello",
        "From: ana@example.org",
        "From: sam@example.org",
    ]
    assert senders(lines) == ["ana", "sam"]


def test_no_from_lines():
    assert senders(["To: a@example.org", "Subject: x"]) == []


def test_empty():
    assert senders([]) == []


def test_similar_header_ignored():
    assert senders(["Reply-From: z@example.org", "From: bo@example.org"]) == ["bo"]
