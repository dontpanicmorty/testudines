from datetime import date

from solution import days_overdue


def test_overdue():
    assert days_overdue(date(2025, 6, 1), 30, date(2025, 7, 11)) == 10


def test_due_today_is_not_overdue():
    assert days_overdue(date(2025, 6, 1), 30, date(2025, 7, 1)) == 0


def test_not_yet_due():
    assert days_overdue(date(2025, 6, 1), 30, date(2025, 6, 15)) == 0


def test_across_leap_day():
    assert days_overdue(date(2024, 2, 1), 30, date(2024, 3, 10)) == 8
