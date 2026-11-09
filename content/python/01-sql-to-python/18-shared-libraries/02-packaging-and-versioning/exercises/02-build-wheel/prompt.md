Build a wheel by hand. Write `build_wheel(package_dir, dist_name, version, out_dir)` from scratch.

- `package_dir` is a directory like `src/acme_datakit` containing Python files (possibly in sub-packages).
- Create `out_dir/{import_name}-{version}-py3-none-any.whl`, where `import_name` is `dist_name` with `-` replaced by `_`. Create `out_dir` if needed. Return the wheel's `Path`.
- Inside the zip: every `*.py` file under `package_dir`, stored as `{package_name}/relative/path.py` (the package folder's own name first, forward slashes), plus `{import_name}-{version}.dist-info/METADATA` containing exactly these lines:

```
Metadata-Version: 2.1
Name: <dist_name>
Version: <version>
```

(each line ends with a newline). Ignore non-`.py` files and `__pycache__`.

```python
build_wheel(Path("src/acme_datakit"), "acme-datakit", "1.4.2", Path("dist"))
# dist/acme_datakit-1.4.2-py3-none-any.whl
```
