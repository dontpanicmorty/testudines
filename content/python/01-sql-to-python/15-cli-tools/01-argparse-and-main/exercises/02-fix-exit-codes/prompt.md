`main(argv)` counts the non-blank data lines in a file (`rowcount orders.csv`), printing the number. With `--skip-header` it does not count the first line.

The orchestrator reports the task green even when the file does not exist, and downstream tools receive the error text as if it were the count. Fix the program so that:

- on success it prints only the number to stdout and **returns** `0`;
- if the file cannot be read it prints one line starting with `error:` to **stderr**, prints nothing to stdout, and returns `1`;
- it never calls `sys.exit` itself (the `__main__` guard does that).

```python
main(["orders.csv"])                    # prints 42, returns 0
main(["nope.csv"])                      # stderr: "error: cannot read nope.csv ...", returns 1
```
