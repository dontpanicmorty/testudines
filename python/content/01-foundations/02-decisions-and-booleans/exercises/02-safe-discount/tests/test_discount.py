from solution import apply_discount


def test_normal():
    assert apply_discount(200.0, 25) == 150.0
    assert apply_discount(19.99, 10) == 17.99


def test_none_means_no_discount():
    assert apply_discount(200.0, None) == 200.0


def test_zero():
    assert apply_discount(200.0, 0) == 200.0


def test_full_discount():
    assert apply_discount(50.0, 100) == 0.0


def test_out_of_range_ignored():
    assert apply_discount(200.0, 150) == 200.0
    assert apply_discount(200.0, -5) == 200.0
