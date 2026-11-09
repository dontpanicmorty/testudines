from solution import gigabytes_needed


def test_whole_number():
    assert gigabytes_needed(500, 4) == 2.0


def test_fraction():
    assert gigabytes_needed(250, 2) == 0.5


def test_no_photos():
    assert gigabytes_needed(0, 5) == 0


def test_large_photos():
    assert gigabytes_needed(10, 3.5) == 0.035
