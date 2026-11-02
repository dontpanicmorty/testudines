import typer

app = typer.Typer()


@app.command()
def greet(name: str, upper: bool = False):
    text = f"Hello, {name}!"
    typer.echo(text.upper() if upper else text)


@app.command()
def repeat(text: str, times: int = 2):
    for _ in range(times):
        typer.echo(text)


if __name__ == "__main__":
    app()
