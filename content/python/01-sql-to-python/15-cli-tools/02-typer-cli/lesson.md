+++
id = "cli-tools.typer-cli"
title = "Typer: CLIs from type hints"
minutes = 25
+++

# Typer: CLIs from type hints

`argparse` makes you describe every argument twice: once in the function and once in the parser. **Typer** reads your function's **type hints** and builds the interface from them. A parameter with no default becomes a required argument; one with a default becomes an option; a `bool` becomes a flag. It also gives you subcommands (`tool load`, `tool check`), the way `dbt` has `run`, `test` and `build`.

> **dbt bridge.** `dbt run`, `dbt test`, `dbt docs` are subcommands of one program. Each Typer `@app.command()` is one of those.

## One function, one command

```python
import typer
from typer.testing import CliRunner

app = typer.Typer()

@app.command()
def hello(name: str, times: int = 1, shout: bool = False):
    """Greet NAME."""
    for _ in range(times):
        text = f"Hello, {name}!"
        typer.echo(text.upper() if shout else text)

@app.command()
def bye(name: str):
    typer.echo(f"Bye, {name}.")

runner = CliRunner()
result = runner.invoke(app, ["hello", "Ada", "--times", "2", "--shout"])
print(result.exit_code)
print(result.stdout)
```

Mapping: `name: str` is a required argument; `times: int = 1` becomes `--times`; `shout: bool = False` becomes the flag `--shout` (and `--no-shout`). Types convert and validate for free.

With only one command, Typer treats it as the whole program (no subcommand word). Add a second and the names appear. In this lesson there are two.

## Testing with CliRunner

`CliRunner` runs your app **in-process**: no subprocess, no shell, fully deterministic. `invoke` returns a result with `exit_code`, `stdout`, `stderr`.

```python
import typer
from typer.testing import CliRunner

app = typer.Typer()

@app.command()
def add(a: int, b: int):
    typer.echo(a + b)

@app.command()
def noop():
    pass

runner = CliRunner()
ok = runner.invoke(app, ["add", "2", "3"])
print(ok.exit_code, repr(ok.stdout))

bad = runner.invoke(app, ["add", "2", "three"])
print(bad.exit_code)
print("Invalid value" in bad.output or "not a valid integer" in bad.output)
```

> **Predict first.** What exit code does a type conversion failure produce?

`2`, the usage-error code, same convention as argparse.

## Options with metadata

When you need help text, bounds or choices, wrap the default in `typer.Option` or `typer.Argument`. Use an `Enum` for a fixed set of values.

```python
from enum import Enum
import typer
from typer.testing import CliRunner

class Env(str, Enum):
    dev = "dev"
    prod = "prod"

app = typer.Typer()

@app.command()
def run(
    batch: int = typer.Option(500, "--batch-size", min=1, help="Rows per batch"),
    env: Env = Env.dev,
):
    typer.echo(f"env={env.value} batch={batch}")

@app.command()
def other():
    pass

r = CliRunner()
print(r.invoke(app, ["run", "--env", "prod"]).stdout.strip())
print(r.invoke(app, ["run", "--batch-size", "0"]).exit_code)
print(r.invoke(app, ["run", "--env", "qa"]).exit_code)
```

`min=1` and the enum give the validation that you wrote by hand with `choices=` and `if` statements in argparse.

## Exit codes and errors

Raise `typer.Exit(code=...)` to stop with a status. Write errors with `err=True` so they go to stderr:

```python
import typer
from typer.testing import CliRunner

app = typer.Typer()

@app.command()
def check(value: int = 0):
    if value < 0:
        typer.echo("error: value must be >= 0", err=True)
        raise typer.Exit(code=1)
    typer.echo("ok")

@app.command()
def noop():
    pass

r = CliRunner().invoke(app, ["check", "--value", "-5"])
print(r.exit_code, repr(r.stdout), repr(r.stderr))
```

A plain `raise ValueError` would print a traceback; use `typer.Exit` for failures you expect.

## Running it for real

```python
# no-run
if __name__ == "__main__":
    app()
```

Typer is built on Click and the app object is directly callable. In a packaged project you register `app` as a console script so users type `mytool hello Ada`.

## Keep the logic out of the command

The command function is a thin adapter: parse input, call a plain function, format output, choose an exit code. The plain function is easy to unit-test with no CLI at all.

```python
import typer
from typer.testing import CliRunner

def total(values: list[int]) -> int:           # pure, trivially testable
    return sum(values)

app = typer.Typer()

@app.command()
def sum_(values: list[int]):
    typer.echo(total(values))

@app.command()
def noop():
    pass

print(CliRunner().invoke(app, ["sum-", "1", "2", "3"]).stdout.strip())
```

Notice the function name `sum_` became the command `sum-`. Typer converts underscores to dashes. Set an explicit name with `@app.command("sum")` when you want something else.

## Common mistakes

- Testing a one-command app with the command name: `invoke(app, ["hello", "Ada"])` treats `hello` as the first argument. Add a second command or call it without the name.
- Forgetting `err=True` and sending errors to stdout.
- A `bool` parameter without a default is a required argument, not a flag. Give it `= False`.
- Using bare `int` where `min=1` belongs: `--batch-size 0` is accepted and loops forever.
- `Error: No such option: --batch_size`: Typer uses dashes, not underscores, in option names.
- Business logic inside the command, which can only be tested through the CLI.

## What to take away

1. Type hints define the CLI: no default is an argument, a default makes an option, `bool` makes a flag.
2. `Enum` and `typer.Option(min=...)` provide validation declaratively.
3. `CliRunner.invoke(app, [...])` tests the whole interface in-process; check `exit_code`, `stdout`, `stderr`.
4. Raise `typer.Exit(code)` for expected failures; use `typer.echo(..., err=True)` for errors.
5. Keep commands thin and put logic in plain functions.
