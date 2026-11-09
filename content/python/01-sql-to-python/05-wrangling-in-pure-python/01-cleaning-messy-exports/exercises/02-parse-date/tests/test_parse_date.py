from datetime import date

import pytest

from solution import parse_date


def test_iso():
    assert parse_date("2025-09-26") == date(2025, 9, 26)


def test_day_month_name():
    assert parse_date("20 Jun 2025") == date(2025, 6, 20)
    assert parse_date("05 Mar 2025") == date(2025, 3, 5)


def test_us_slashes():
    assert parse_date("05/26/2025") == date(2025, 5, 26)
    assert parse_date("07/07/2025") == date(2025, 7, 7)


def test_whitespace():
    assert parse_date("  2025-01-02 ") == date(2025, 1, 2)


def test_result_is_date_not_datetime():
    from datetime import datetime

    assert not isinstance(parse_date("2025-09-26"), datetime)


@pytest.mark.parametrize("bad", ["26/05/2025", "yesterday", "", "2025-13-01"])
def test_bad(bad):
    with pytest.raises(ValueError) as exc:
        parse_date(bad)
    assert repr(bad)[1:-1] in str(exc.value) or bad in str(exc.value)
