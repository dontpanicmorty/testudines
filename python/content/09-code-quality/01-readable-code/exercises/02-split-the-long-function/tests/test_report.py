import ast
from pathlib import Path

import pytest

from solution import process

CASES = [
    ("customer,amount,status\nAda,$10.5,paid\nGrace,3,open\nAda,2,PAID", "Ada: 12.50\nTOTAL: 12.50"),
    (
        "customer,amount,status\nGrace,5,paid\nAda,5,paid\nLinus,9.99,paid",
        "Linus: 9.99\nAda: 5.00\nGrace: 5.00\nTOTAL: 19.99",
    ),
    ("status,customer,amount\npaid, Ada ,$1,000".replace("$1,000", "$1000"), "Ada: 1000.00\nTOTAL: 1000.00"),
    ("customer,amount,status\nAda,5,open\n", "TOTAL: 0.00"),
    ("customer,amount,status\nAda,5,paid\n\nGrace,1, Paid \n", "Ada: 5.00\nGrace: 1.00\nTOTAL: 6.00"),
]


@pytest.mark.parametrize("text, expected", CASES)
def test_behaviour_is_unchanged(text, expected):
    assert process(text) == expected


def functions():
    tree = ast.parse(Path("solution.py").read_text())
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def test_at_least_three_functions():
    assert len(functions()) >= 3, "Split process into at least three functions."


def test_no_function_is_longer_than_fifteen_lines():
    too_long = {f.name: f.end_lineno - f.lineno + 1 for f in functions() if f.end_lineno - f.lineno + 1 > 15}
    assert not too_long, f"These functions are longer than 15 lines: {too_long}"
