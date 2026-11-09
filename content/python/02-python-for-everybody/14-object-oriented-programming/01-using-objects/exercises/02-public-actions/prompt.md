Write `actions(obj)` that returns a sorted list of the names of the object's methods you would call yourself: names that do **not** start with an underscore and that refer to something callable.

```python
actions("abc")   # includes "upper", "split", "strip" ...
actions([])      # includes "append", "sort" but not "__len__"
```

Plain data attributes (such as a number stored on an object) must be excluded.
