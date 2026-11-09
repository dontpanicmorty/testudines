Write `summarize PATH --column NAME` (default column `amount`) as a Typer command (a second command `version` is provided).

It reads a CSV with a header and prints two lines to stdout:

```
rows=3
sum=60.50
```

- `rows` counts data rows; `sum` totals the numeric column, formatted with two decimals. Blank cells count as 0.
- A missing file: print `error: ...` to **stderr**, nothing to stdout, exit code `1`.
- A column that is not in the header: same, exit code `1`, and the message names the column.
- A non-numeric value in the column: same, exit code `1`.

Also expose the plain function `summarize_csv(path, column) -> tuple[int, float]` so the logic can be tested without the CLI. It raises `FileNotFoundError` or `ValueError` for the failures above.
