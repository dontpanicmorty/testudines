from solution import LendingDesk


def test_lend_and_list():
    d = LendingDesk()
    assert d.lend("Reed Songs", "ines") is True
    assert d.lend("Tide Tables", "ines") is True
    assert d.titles_for("ines") == ["Reed Songs", "Tide Tables"]
    assert d.on_loan_count() == 2


def test_double_lend_refused():
    d = LendingDesk()
    d.lend("Reed Songs", "ines")
    assert d.lend("Reed Songs", "omar") is False
    assert d.titles_for("omar") == []
    assert d.titles_for("ines") == ["Reed Songs"]


def test_give_back():
    d = LendingDesk()
    d.lend("Reed Songs", "ines")
    assert d.give_back("Reed Songs") is True
    assert d.give_back("Reed Songs") is False
    assert d.on_loan_count() == 0
    assert d.lend("Reed Songs", "omar") is True


def test_desks_are_separate():
    a, b = LendingDesk(), LendingDesk()
    a.lend("X", "m")
    assert b.on_loan_count() == 0
    assert b.lend("X", "n") is True


def test_unknown_member():
    assert LendingDesk().titles_for("nobody") == []
