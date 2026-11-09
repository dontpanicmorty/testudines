from solution import each_pays


def test_basic():
    assert abs(each_pays(60, 10, 3) - 22.0) < 1e-9


def test_no_tip():
    assert each_pays(40, 0, 4) == 10


def test_one_person():
    assert abs(each_pays(50, 20, 1) - 60.0) < 1e-9


def test_free_meal():
    assert each_pays(0, 15, 2) == 0
