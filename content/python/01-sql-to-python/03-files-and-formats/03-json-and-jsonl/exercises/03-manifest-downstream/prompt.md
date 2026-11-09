Given a dbt-style manifest dict (`manifest["nodes"][unique_id]["depends_on"]["nodes"]` lists parents; some nodes may have no `depends_on` or no `nodes` key), write `downstream_models(manifest, node_id)` that returns a **sorted list** of the unique ids of all models that depend on `node_id`, directly or indirectly. Only ids starting with `"model."` are returned, and the starting node itself is never included. Sources and parents may be missing from `nodes`.

```python
# stg_orders <- int_totals <- fct_sales ; stg_orders <- fct_sales
downstream_models(manifest, "model.shop.stg_orders")
# ["model.shop.fct_sales", "model.shop.int_totals"]
```
