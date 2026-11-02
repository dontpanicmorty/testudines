A dbt-style graph maps each node to the nodes it **depends on**. Before changing a staging model you want to know what could break.

Write `downstream(graph, node)` returning the **set** of all nodes that depend on `node`, directly or transitively (not including `node` itself).

```python
graph = {
    "stg_orders": [],
    "fct_orders": ["stg_orders"],
    "report": ["fct_orders"],
    "other": [],
}
downstream(graph, "stg_orders")   # {"fct_orders", "report"}
downstream(graph, "report")       # set()
```
