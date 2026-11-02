Write the heart of a dbt-like renderer.

`render(template, relations)` replaces every `{{ ref('model') }}` (single or double quotes, any spaces inside the braces or parentheses) with `relations["model"]`. If a model is not in `relations`, raise `KeyError` whose message contains the model name.

`refs_in(template)` returns the list of model names referenced, in order of first appearance, without duplicates.

```python
render("SELECT * FROM {{ ref('orders') }}", {"orders": "main.orders"})  # "SELECT * FROM main.orders"
refs_in("{{ ref('a') }} {{ref(\"b\")}} {{ ref('a') }}")                  # ["a", "b"]
```
