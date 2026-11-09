from solution import addresses


def write(tmp_path, text):
    p = tmp_path / "net.txt"
    p.write_text(text, encoding="utf-8")
    return p


def test_basic(tmp_path):
    p = write(tmp_path, "hosts: 10.0.0.1 and 192.168.1.20\nlater 10.0.0.1 again\n")
    assert addresses(p) == ["10.0.0.1", "192.168.1.20", "10.0.0.1"]


def test_none(tmp_path):
    assert addresses(write(tmp_path, "version 3.11 only\n")) == []


def test_empty(tmp_path):
    assert addresses(write(tmp_path, "")) == []


def test_dot_is_literal(tmp_path):
    assert addresses(write(tmp_path, "1x2x3x4\n")) == []


def test_embedded_in_text(tmp_path):
    p = write(tmp_path, "from=1.2.3.4;to=5.6.7.8.\n")
    assert addresses(p) == ["1.2.3.4", "5.6.7.8"]
