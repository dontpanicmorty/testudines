import subprocess
import sys

import pytest

from solution import normalize_headers


def ruff(*args):
    return subprocess.run(
        [sys.executable, "-m", "ruff", *args, "--isolated", "solution.py"],
        capture_output=True, text=True, timeout=60,
    )


@pytest.mark.parametrize(
    "headers, expected",
    [
        (["Order ID", " Total ($) ", "total", "", "TOTAL"], ["order_id", "total", "total_2", "col_3", "total_3"]),
        (["a-b", "A  B", "__x__"], ["a_b", "a_b_2", "x"]),
        (["", " ", "!!"], ["col_0", "col_1", "col_2"]),
        ([], []),
        (["Total", "Total", "Total"], ["total", "total_2", "total_3"]),
    ],
)
def test_headers(headers, expected):
    assert normalize_headers(headers) == expected


def test_input_is_not_modified():
    headers = ["A", "a"]
    normalize_headers(headers)
    assert headers == ["A", "a"]


def test_ruff_check_is_clean():
    r = ruff("check", "--no-cache", "--select", "E,F,I,B,UP,SIM,N,C4", "--output-format", "concise")
    assert r.returncode == 0, "ruff check reports problems:\n" + r.stdout


def test_ruff_format_is_clean():
    r = ruff("format", "--check", "--diff")
    assert r.returncode == 0, "ruff format would change your file:\n" + r.stdout
