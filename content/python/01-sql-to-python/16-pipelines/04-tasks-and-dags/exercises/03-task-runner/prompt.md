Write `run_tasks(tasks, deps)`.

- `tasks`: dict of name to a zero-argument callable.
- `deps`: dict of name to the list of names it depends on (a task missing from `deps` has no dependencies).
- Run every task in dependency order. Break ties alphabetically so order is deterministic.
- A task runs only if **all** its dependencies succeeded. Otherwise it is `"skipped"` and its callable is not called.
- If a task raises, its status is `"failed"` and the runner continues with the others (they may still run if unrelated).
- Return `{name: "success" | "failed" | "skipped"}` for every task.
- A cycle raises `ValueError` **before** any task runs.

```python
run_tasks({"a": fail, "b": ok, "c": ok}, {"b": ["a"]})
# {"a": "failed", "b": "skipped", "c": "success"}
```
