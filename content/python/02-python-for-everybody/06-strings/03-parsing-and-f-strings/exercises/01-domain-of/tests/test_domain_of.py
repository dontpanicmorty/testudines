from solution import domain_of


def test_basic():
    assert domain_of("sam@example.org") == "example.org"


def test_subdomain():
    assert domain_of("a.b@mail.example.org") == "mail.example.org"


def test_nothing_after_at():
    assert domain_of("x@") == ""
