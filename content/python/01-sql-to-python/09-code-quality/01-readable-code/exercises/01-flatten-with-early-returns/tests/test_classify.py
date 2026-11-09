import ast
from pathlib import Path

import pytest

from solution import classify_order


@pytest.mark.parametrize(
    "order, expected",
    [
        (None, "missing"),
        ({"status": "open", "total": 50, "country": "US"}, "open"),
        ({}, "open"),
        ({"status": "complete", "total": 0, "country": "US"}, "empty"),
        ({"status": "complete", "total": -5, "country": "US"}, "empty"),
        ({"status": "complete", "country": "US"}, "empty"),
        ({"status": "complete", "total": 50, "country": "US"}, "domestic"),
        ({"status": "complete", "total": 50, "country": "FR"}, "international"),
        ({"status": "complete", "total": 50}, "international"),
    ],
)
def test_behaviour_is_unchanged(order, expected):
    assert classify_order(order) == expected


def depth_of(stmts, level):
    best = level
    for stmt in stmts:
        if isinstance(stmt, ast.If):
            best = max(best, depth_of(stmt.body, level + 1))
            orelse = stmt.orelse
            while len(orelse) == 1 and isinstance(orelse[0], ast.If):
                best = max(best, depth_of(orelse[0].body, level + 1))
                orelse = orelse[0].orelse
            best = max(best, depth_of(orelse, level + 1))
        elif isinstance(stmt, (ast.For, ast.While, ast.With, ast.Try)):
            blocks = [stmt.body, stmt.orelse] if not isinstance(stmt, ast.With) else [stmt.body]
            if isinstance(stmt, ast.Try):
                blocks += [stmt.finalbody] + [h.body for h in stmt.handlers]
            for block in blocks:
                best = max(best, depth_of(block, level + 1))
    return best


def test_nesting_is_at_most_two_levels():
    tree = ast.parse(Path("solution.py").read_text())
    func = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "classify_order")
    depth = depth_of(func.body, 0)
    assert depth <= 2, f"classify_order nests {depth} levels deep; flatten it with early returns"
