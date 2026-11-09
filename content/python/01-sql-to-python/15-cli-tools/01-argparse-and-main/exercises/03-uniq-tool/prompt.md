Write a small `dedupe` tool as `main(argv=None, *, stdin=None, stdout=None, stderr=None) -> int` (each stream defaults to the real `sys.stdin/stdout/stderr`, so tests can pass `io.StringIO`).

Command line: `dedupe [PATH] [--ignore-case] [--count]`

- `PATH` is optional and defaults to `-`, meaning read from `stdin`. Otherwise read the file.
- Blank lines (after stripping the newline) are skipped; lines are otherwise compared exactly.
- Output the **first occurrence** of each distinct line, in original order, one per line, to `stdout`.
- `--ignore-case` treats `A` and `a` as the same line (the first spelling is printed).
- `--count` prefixes each output line with its total count and a tab: `3\tapple`.
- Unreadable file: write `error: ...` to `stderr`, nothing to stdout, return `1`. Success returns `0`. Bad usage is left to argparse (exit code 2).

```python
main(["--count"], stdin=io.StringIO("a\nb\na\n"), stdout=out)   # out gets "2\ta\n1\tb\n"
```
