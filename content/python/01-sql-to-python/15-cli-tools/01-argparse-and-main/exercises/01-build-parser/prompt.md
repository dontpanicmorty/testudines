Write `build_parser()` returning an `argparse.ArgumentParser` for a tool called `export_orders`:

- positional `input` (a path string);
- `-o` / `--output`, default `"-"` (meaning stdout);
- `--limit`, an `int`, default `None`;
- `--env`, one of `dev` or `prod`, default `dev`;
- `--dry-run`, a flag that is `False` unless present.

```python
args = build_parser().parse_args(["orders.csv", "-o", "out.csv", "--limit", "10", "--dry-run"])
args.input, args.output, args.limit, args.dry_run   # ("orders.csv", "out.csv", 10, True)
```

Invalid values (`--limit abc`, `--env staging`) must make argparse exit with code 2, which comes for free from the right `type` and `choices`.
