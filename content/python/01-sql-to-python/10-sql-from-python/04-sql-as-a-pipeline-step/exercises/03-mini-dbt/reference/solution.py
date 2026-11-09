import re
from graphlib import CycleError, TopologicalSorter

import duckdb

REF = re.compile(r"""\{\{\s*ref\(\s*(['"])([^'"]+)\1\s*\)\s*\}\}""")


def run_models(con: duckdb.DuckDBPyConnection, models: dict[str, str]) -> list[str]:
    """Render ref() templates, order by dependency, build each as a table."""
    graph: dict[str, set[str]] = {}
    for name, template in models.items():
        parents = {m.group(2) for m in REF.finditer(template)}
        missing = parents - models.keys()
        if missing:
            raise KeyError(f"model {name!r} refs unknown model(s): {sorted(missing)}")
        graph[name] = parents
    try:
        order = list(TopologicalSorter(graph).static_order())
    except CycleError as exc:
        raise ValueError(f"dependency cycle: {exc.args[1]}") from exc
    for name in order:
        sql = REF.sub(lambda m: m.group(2), models[name])
        con.execute(f"CREATE OR REPLACE TABLE {name} AS {sql}")
    return order
