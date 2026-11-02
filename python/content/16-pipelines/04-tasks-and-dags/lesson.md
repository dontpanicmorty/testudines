+++
id = "pipelines.tasks-and-dags"
title = "Tasks and dependency graphs"
minutes = 35
+++

# Tasks and dependency graphs

dbt builds a DAG from your `ref()` calls and runs models in an order that respects it. Orchestrators do the same for arbitrary tasks. In this lesson you build the core of that machine yourself, in about forty lines, with no orchestrator library.

> **dbt bridge.** `ref('stg_orders')` inside `fct_orders` declares an edge `stg_orders -> fct_orders`. dbt topologically sorts the graph, runs independent models in parallel, and on failure skips everything downstream. `dbt run --select +fct_orders` means "this node and everything upstream". You are about to write each of those ideas.

## A graph as a dict

The simplest representation: each task maps to the list of tasks it **depends on**.

```python
graph = {
    "stg_orders": [],
    "stg_customers": [],
    "dim_customers": ["stg_customers"],
    "fct_orders": ["stg_orders", "dim_customers"],
    "report": ["fct_orders"],
}
print(graph["fct_orders"])
```

A node with no dependencies is a **root** (a source). Direction matters: *upstream* of `fct_orders` is what it depends on; *downstream* is what depends on it.

## Walking the graph

Upstream of a node is its dependencies, their dependencies, and so on. A stack or recursion does it, and a `seen` set stops you visiting twice.

```python
graph = {
    "stg_orders": [], "stg_customers": [],
    "dim_customers": ["stg_customers"],
    "fct_orders": ["stg_orders", "dim_customers"],
    "report": ["fct_orders"],
}

def upstream(graph, node):
    seen = set()
    stack = list(graph[node])
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            stack.extend(graph[n])
    return seen

print(sorted(upstream(graph, "report")))
print(sorted(upstream(graph, "dim_customers")))
```

That is `dbt ... --select +report`. Downstream is the same walk over the reversed graph.

## Topological sort

A **topological order** lists every node after all of its dependencies. One standard algorithm (Kahn's) repeatedly takes nodes with no unmet dependencies.

> **Predict first.** For the graph above, which node must come last? Which two could come first?

```python
def topo_sort(graph):
    remaining = {n: set(deps) for n, deps in graph.items()}
    order = []
    while remaining:
        ready = sorted(n for n, deps in remaining.items() if not deps)
        if not ready:
            raise ValueError(f"cycle among: {sorted(remaining)}")
        node = ready[0]            # sorted() makes the order deterministic
        order.append(node)
        del remaining[node]
        for deps in remaining.values():
            deps.discard(node)
    return order

graph = {
    "stg_orders": [], "stg_customers": [],
    "dim_customers": ["stg_customers"],
    "fct_orders": ["stg_orders", "dim_customers"],
    "report": ["fct_orders"],
}
print(topo_sort(graph))

try:
    topo_sort({"a": ["b"], "b": ["a"]})
except ValueError as exc:
    print(exc)
```

Two details earn their keep. `sorted(...)` removes arbitrary tie-breaking so the same graph always gives the same order (determinism again). And if nothing is ready while nodes remain, every remaining node is waiting on another remaining node: a **cycle**. `a -> b -> a` has no valid order, and a good tool says so clearly (the last lines of the example above show the error).

## A tiny task runner

A task is just a callable. The runner sorts, then calls each task in order. The interesting question is failure: if `stg_orders` fails, `fct_orders` has no valid input and must not run, but `dim_customers` is unrelated and should.

```python
def topo_sort(graph):
    remaining = {n: set(d) for n, d in graph.items()}
    order = []
    while remaining:
        ready = sorted(n for n, d in remaining.items() if not d)
        if not ready:
            raise ValueError("cycle")
        order.append(ready[0])
        del remaining[ready[0]]
        for d in remaining.values():
            d.discard(order[-1])
    return order

def run(tasks, graph):
    status = {}
    for name in topo_sort(graph):
        if any(status[dep] != "success" for dep in graph[name]):
            status[name] = "skipped"
            continue
        try:
            tasks[name]()
            status[name] = "success"
        except Exception:
            status[name] = "failed"
    return status

def boom():
    raise RuntimeError("warehouse down")

graph = {"a": [], "b": ["a"], "c": [], "d": ["b", "c"]}
tasks = {"a": boom, "b": print, "c": lambda: None, "d": print}
print(run(tasks, graph))
```

Because we walk in topological order, by the time a task is considered every dependency already has a status. One rule covers failures and skips: run only if all dependencies succeeded, otherwise skip.

## How this maps to real orchestrators

What you just wrote is the skeleton of every scheduler:

| Your code | Orchestrator concept |
|---|---|
| `graph` dict | the DAG definition |
| a callable | a task / operator |
| `status` dict | task instance state |
| skip on failed dependency | `upstream_failed` / skipped state |
| `topo_sort` | the scheduler's ordering step |

Real tools add: running independent tasks in parallel, persisting state between runs, retries per task (lesson 3), schedules, and a UI. They do not change the core idea. Knowing it makes their configuration predictable: when a task "didn't run", you know to look for a failed or skipped upstream node.

**Tasks should be idempotent and take their logical date as an argument**, so a scheduler can rerun any node without special handling. That is lessons 1 and 2 paying off.

## Common mistakes

- Forgetting a dependency edge: the DAG runs happily in the wrong order, and the bug appears only when timing changes.
- Declaring a dependency on a node that is not in the graph: `KeyError: 'stg_missing'`. Validate that every dependency is a defined node.
- Mutating the input graph while sorting. Copy first (`set(deps)`).
- Treating "skipped" as "success". Downstream of a skip is also a skip.

## What to take away

1. A DAG is a dict of node to dependencies; direction is dependency to dependent.
2. Upstream and downstream are graph walks with a `seen` set.
3. Kahn's algorithm: repeatedly emit nodes with no unmet dependencies; if none are ready, there is a cycle.
4. A runner is a topological loop plus one rule: run only if all dependencies succeeded.
5. Orchestrators and dbt add scale and persistence around this same core.
