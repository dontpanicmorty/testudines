from solution import tidy


def test_messy():
    assert tidy("  aDA lovelace ") == "Ada Lovelace"


def test_already_tidy():
    assert tidy("Grace Hopper") == "Grace Hopper"


def test_blank_only():
    assert tidy("    ") == ""


def test_single_word():
    assert tidy("PLATO") == "Plato"
