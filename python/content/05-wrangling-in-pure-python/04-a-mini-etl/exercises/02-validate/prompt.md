Stages one and two. `read_valid(path)` reads a CSV with `order_id,customer_id,sku,quantity,unit_price` and returns `(valid, rejects)`.

A row is valid when: `order_id` is non-blank, `customer_id` is an integer, `sku` is non-blank, `quantity` is a positive integer, `unit_price` is a Decimal that is not negative. Valid rows become `{"order_id": str, "customer_id": int, "sku": str (stripped, uppercase), "quantity": int, "unit_price": Decimal}`.

Each reject is `{"line": <line number in the file, header is line 1>, "reason": <str>}`. The reason must mention **every** failing field by name (for example `customer_id`, `quantity`), joined with `"; "`. Keep the order of the file.

```python
# line 2: A1,1,x-100,2,5.00      -> valid
# line 3: A2,two,y-200,0,5.00    -> reject: "customer_id ...; quantity ..."
```
