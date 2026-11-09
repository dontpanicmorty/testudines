from solution import parse_line


def test_basic():
    assert parse_line("2026-03-01 14:22:05 [WARN] cache is cold") == {
        "date": "2026-03-01",
        "time": "14:22:05",
        "level": "WARN",
        "message": "cache is cold",
    }


def test_garbage():
    assert parse_line("hello world") is None


def test_lowercase_level_rejected():
    assert parse_line("2026-03-01 14:22:05 [warn] x") is None


def test_missing_message():
    assert parse_line("2026-03-01 14:22:05 [INFO] ") is None


def test_message_with_brackets():
    result = parse_line("2026-03-01 14:22:05 [INFO] got [x] ok")
    assert result["message"] == "got [x] ok"
    assert result["level"] == "INFO"


def test_bad_date_shape():
    assert parse_line("26-3-1 14:22:05 [INFO] hi") is None
