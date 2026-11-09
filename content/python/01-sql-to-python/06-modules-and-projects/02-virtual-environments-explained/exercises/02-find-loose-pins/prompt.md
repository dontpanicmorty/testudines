Before deploying a pipeline, the team wants to know which dependencies are **not** pinned to an exact version.

Write `unpinned(text)` that takes the contents of a requirements file and returns a **sorted list of lower-cased package names** that are not pinned with `==`.

Rules:

- ignore blank lines, comment lines, and inline `# comments`;
- ignore option lines that start with `-` (such as `-r base.txt`);
- extras like `pandas[performance]>=2` count as the package `pandas`;
- environment markers (`; python_version < "3.13"`) don't change whether it's pinned.

```python
text = """
# core
Pandas>=2.0
requests==2.32.3  # pinned
-r base.txt
duckdb
httpx[http2]~=0.27
"""
unpinned(text)   # ['duckdb', 'httpx', 'pandas']
```
