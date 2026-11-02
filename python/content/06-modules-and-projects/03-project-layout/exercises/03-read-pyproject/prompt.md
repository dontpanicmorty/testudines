A repo-audit script needs to summarise projects. Write `project_info(text)` taking the text of a `pyproject.toml` and returning a dict:

- `"name"` and `"version"` from `[project]`;
- `"dependencies"`: list of **lower-cased package names** in file order, without versions, extras or markers (missing key means `[]`);
- `"scripts"`: dict mapping each command to a `(module, function)` tuple (missing means `{}`).

If there is no `[project]` table, raise `ValueError("missing [project] table")`.

```python
text = '''
[project]
name = "mylib"
version = "0.1.0"
dependencies = ["Pandas>=2.0", "httpx[http2]>=0.27"]
[project.scripts]
ingest = "mylib.cli:main"
'''
project_info(text)
# {'name': 'mylib', 'version': '0.1.0', 'dependencies': ['pandas', 'httpx'],
#  'scripts': {'ingest': ('mylib.cli', 'main')}}
```
