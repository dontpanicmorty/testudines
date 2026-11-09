from solution import average_ms


def write(tmp_path, text):
    p = tmp_path / "log.txt"
    p.write_text(text, encoding="utf-8")
    return p


def test_basic(tmp_path):
    p = write(tmp_path, "GET /a took 100 ms\nnoise\nGET /b took 200 ms\n")
    assert average_ms(p) == 150.0


def test_no_matches(tmp_path):
    assert average_ms(write(tmp_path, "nothing\n")) == 0.0


def test_empty(tmp_path):
    assert average_ms(write(tmp_path, "")) == 0.0


def test_first_duration_only(tmp_path):
    p = write(tmp_path, "took 10 ms then took 999 ms\n")
    assert average_ms(p) == 10.0


def test_fraction(tmp_path):
    p = write(tmp_path, "took 1 ms\ntook 2 ms\n")
    assert average_ms(p) == 1.5


def test_wrong_unit_ignored(tmp_path):
    p = write(tmp_path, "took 5 s\ntook 8 ms\n")
    assert average_ms(p) == 8.0
