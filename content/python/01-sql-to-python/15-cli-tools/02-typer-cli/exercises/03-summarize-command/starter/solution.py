import csv
from pathlib import Path

import typer

app = typer.Typer()


def summarize_csv(path: Path, column: str) -> tuple[int, float]:
    """Return (row_count, total) for a numeric column. Raise on problems."""
    raise NotImplementedError


@app.command()
def summarize(path: Path, column: str = "amount"):
    # TODO: call summarize_csv, print rows= and sum=, handle failures
    raise NotImplementedError


@app.command()
def version():
    typer.echo("1.0")


if __name__ == "__main__":
    app()
