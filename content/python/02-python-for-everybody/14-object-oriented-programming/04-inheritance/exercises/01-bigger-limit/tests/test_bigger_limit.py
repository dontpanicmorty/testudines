from solution import Member, Staff, Student


def test_plain_member():
    assert Member("Omar").summary() == "Omar: 3"


def test_student():
    assert Student("Ines").summary() == "Ines: 5"
    assert Student("Ines").loan_limit() == 5


def test_staff():
    assert Staff("Kai").summary() == "Kai: 10"


def test_relationship():
    assert issubclass(Student, Member)
    assert issubclass(Staff, Member)
    assert isinstance(Student("x"), Member)


def test_summary_not_copied():
    assert "summary" not in Student.__dict__
    assert "summary" not in Staff.__dict__
