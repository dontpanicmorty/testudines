import json

import typer

app = typer.Typer()


@app.command()
def sample(count: int = 3, format: str = "csv"):
    if format == "json":
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
