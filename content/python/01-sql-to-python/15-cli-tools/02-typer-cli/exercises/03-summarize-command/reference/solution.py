import csv
from pathlib import Path

import typer

app = typer.Typer()


def summarize_csv(path: Path, column: str) -> tuple[int, float]:
    """Return (row_count, total) for a numeric column. Raise on problems."""
    path = Path(path)
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or column not in reader.fieldnames:
            raise ValueError(f"column {column!r} not found")
        rows = 0
        total = 0.0
        for row in reader:
            rows += 1
            cell = (row[column] or "").strip()
            if cell:
                try:
                    total += float(cell)
                except ValueError:
                    raise ValueError(f"row {rows}: {cell!r} is not numeric") from None
    return rows, total


@app.command()
def summarize(path: Path, column: str = "amount"):
    try:
        rows, total = summarize_csv(path, column)
    except (FileNotFoundError, ValueError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"rows={rows}")
    typer.echo(f"sum={total:.2f}")


@app.command()
def version():
    typer.echo("1.0")


if __name__ == "__main__":
    app()
