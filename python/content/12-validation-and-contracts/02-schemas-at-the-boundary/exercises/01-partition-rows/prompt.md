Write `partition(rows, model)` where `rows` is a list of dicts and `model` is any pydantic model class. Return a tuple `(valid, rejects)`:

- `valid`: list of model instances for the rows that validate, in input order.
- `rejects`: list of dicts, one per bad row, in input order: `{"index": position_in_rows, "row": the_original_dict, "errors": [{"field": "a.b", "message": "..."}, ...]}`. `field` joins the error location with dots (`"__row__"` if the location is empty). Include **every** error for the row.

Processing must continue past bad rows.
