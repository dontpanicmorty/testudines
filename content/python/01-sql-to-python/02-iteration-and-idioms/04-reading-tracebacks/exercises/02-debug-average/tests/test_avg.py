from solution import average_amount


def test_basic():
    assert average_amount([{"amount": "10"}, {"amount": "20"}, {"amount": "0"}]) == 15.0


def test_last_row_counted():
    assert average_amount([{"amount": "1"}, {"amount": "3"}]) == 2.0


def test_numeric_comparison_not_string():
    # as strings, "9" > "10" is True and "100" < "20"
    assert average_amount([{"amount": "9"}, {"amount": "100"}]) == 54.5


def test_threshold():
    assert average_amount([{"amount": "0.005"}, {"amount": "0.01"}]) == 0.01


def test_empty_and_none_qualify():
    assert average_amount([]) == 0.0
    assert average_amount([{"amount": "0"}]) == 0.0
