import subprocess
import sys

import pytest


def fresh(code):
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=20)


@pytest.mark.parametrize("first", ["customers", "orders"])
def test_imports_in_either_order(first):
    other = "orders" if first == "customers" else "customers"
    r = fresh(f"import {first}; import {other}")
    assert r.returncode == 0, f"import {first} failed:\n{r.stderr[-400:]}"


def test_order_count():
    r = fresh("import customers; print(customers.order_count(1), customers.order_count(2))")
    assert r.stdout.strip() == "2 1", r.stderr[-400:]


def test_describe_order():
    r = fresh("import orders; print(orders.describe_order(102))")
    assert r.stdout.strip() == "order 102 for Grace", r.stderr[-400:]
