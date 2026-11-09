from solution import compare_versions


def test_numeric_not_text():
    assert compare_versions("1.10", "1.9") == 1
    assert compare_versions("1.9", "1.10") == -1


def test_equal():
    assert compare_versions("2.0.1", "2.0.1") == 0


def test_prefix_is_older():
    assert compare_versions("2.0", "2.0.1") == -1
    assert compare_versions("2.0.1", "2.0") == 1


def test_major_wins():
    assert compare_versions("3.0.0", "2.99.99") == 1


def test_single_numbers():
    assert compare_versions("10", "9") == 1
