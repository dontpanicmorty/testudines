from solution import download_seconds


def test_basic():
    assert download_seconds(100, 50) == 16.0


def test_one_second():
    assert download_seconds(1, 8) == 1.0


def test_empty_file():
    assert download_seconds(0, 25) == 0


def test_slow_line():
    assert download_seconds(5, 2) == 20.0
