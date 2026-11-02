Feeds contain amounts that are junk: `"N/A"`, `""`, `None`. Write `parse_amounts(values)` returning a tuple `(good, rejects)`:

- `good`: list of floats for the values that parse (after stripping whitespace if they are strings)
- `rejects`: list of `(index, original_value)` for the values that could not be parsed

Catch only the specific exceptions float() raises for these inputs. Don't let one bad value stop the run.

```python
parse_amounts(["1.5", " 2 ", "N/A", None, "3"])
# ([1.5, 2.0, 3.0], [(2, "N/A"), (3, None)])
```
