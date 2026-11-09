Write `atomic_write(path, produce)`. It calls `produce(fh)` with a writable text file handle, and the final file at `path` must only ever appear complete.

- Write to a temp file in the **same directory** as `path`, then `os.replace` it over `path`.
- If `produce` raises, the original file (if any) must be left untouched, **no temp files may remain**, and the exception must propagate.

```python
def produce(fh):
    fh.write("id,total\n1,10\n")

atomic_write("/data/daily.csv", produce)
```
