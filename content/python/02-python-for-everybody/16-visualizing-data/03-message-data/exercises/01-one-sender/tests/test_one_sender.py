from solution import clean_sender


def test_display_name():
    assert clean_sender("Ines Ward <INES@Mail.Example.org>") == "ines@mail.example.org"


def test_plain_with_spaces():
    assert clean_sender("  Omar@Club.example.com ") == "omar@club.example.com"


def test_spaces_inside_brackets():
    assert clean_sender("Kai < Kai@Test.Example.net >") == "kai@test.example.net"


def test_already_clean():
    assert clean_sender("a@b.example.org") == "a@b.example.org"
