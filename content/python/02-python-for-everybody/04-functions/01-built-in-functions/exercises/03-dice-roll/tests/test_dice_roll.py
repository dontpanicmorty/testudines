from solution import roll


def test_always_in_range():
    for _ in range(300):
        assert 1 <= roll(6) <= 6


def test_returns_whole_numbers():
    assert all(isinstance(roll(20), int) for _ in range(50))


def test_every_face_appears():
    seen = {roll(4) for _ in range(500)}
    assert seen == {1, 2, 3, 4}


def test_one_sided_die():
    assert roll(1) == 1
