import ast
import copy
from pathlib import Path

from solution import clean


def order(status, total):
    return {"status": status, "total": total}


def test_consecutive_bad_orders_are_all_removed():
    orders = [order("cancelled", 10), order("cancelled", 20), order("paid", 30), order("paid", 0), order("paid", -1)]
    assert clean(orders) == [order("paid", 30)]


def test_order_is_preserved():
    orders = [order("paid", 3), order("open", 2), order("paid", 1)]
    assert clean(orders) == orders


def test_input_is_not_modified():
    orders = [order("cancelled", 10), order("paid", 5)]
    before = copy.deepcopy(orders)
    clean(orders)
    assert orders == before


def test_empty():
    assert clean([]) == []


def test_parameter_has_a_descriptive_name():
    tree = ast.parse(Path("solution.py").read_text())
    func = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "clean")
    names = [a.arg for a in func.args.args]
    assert names and all(len(n) > 1 for n in names), f"Rename single-letter parameters: {names}"
