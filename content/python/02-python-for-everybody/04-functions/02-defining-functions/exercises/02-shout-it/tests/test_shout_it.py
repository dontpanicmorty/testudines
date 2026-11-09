from solution import shout


def test_three_times(capsys):
    shout("go", 3)
    assert capsys.readouterr().out == "GO! GO! GO!\n"


def test_once(capsys):
    shout("hey", 1)
    assert capsys.readouterr().out == "HEY!\n"


def test_zero_times(capsys):
    shout("hey", 0)
    assert capsys.readouterr().out == "\n"


def test_mixed_case(capsys):
    shout("Hello", 2)
    assert capsys.readouterr().out == "HELLO! HELLO!\n"
