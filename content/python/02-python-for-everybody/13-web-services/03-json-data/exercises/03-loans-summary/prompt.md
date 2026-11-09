A loans service sends a JSON array of loans:

```json
[{"member": "ines", "book": "Tide Tables", "days": 14},
 {"member": "omar", "book": "Moss and Stone", "days": 7},
 {"member": "ines", "book": "Reed Songs", "days": 21}]
```

Write `summarize_loans(json_text)` that returns **JSON text** for an object mapping each member to the total number of loan days. Use `sort_keys=True` and no indentation, so the example gives exactly:

```
{"ines": 35, "omar": 7}
```

An empty array gives `{}`.
