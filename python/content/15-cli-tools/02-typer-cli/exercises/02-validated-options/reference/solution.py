import json
from enum import Enum

import typer

app = typer.Typer()


class Format(str, Enum):
    csv = "csv"
    json = "json"


@app.command()
def sample(
    count: int = typer.Option(3, "--count", min=1),
    format: Format = Format.csv,
):
    if format is Format.json:
        for i in range(1, count + 1):
            typer.echo(json.dumps({"id": i, "name": f"user{i}"}))
    else:
        typer.echo("id,name")
        for i in range(1, count + 1):
            typer.echo(f"{i},user{i}")


@app.command()
def version():
    typer.echo("1.0")


if __name__ == "__main__":
    app()
