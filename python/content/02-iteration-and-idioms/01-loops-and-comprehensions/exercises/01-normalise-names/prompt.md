Messy exports have names like `"  aDA lovelace "`. Write `normalise_names(names)` returning a list of names stripped and title-cased (`"Ada Lovelace"`), **skipping** entries that are `None` or blank after stripping. Use a comprehension.

```python
normalise_names(["  aDA lovelace ", "GRACE hopper", "   ", None])
# ["Ada Lovelace", "Grace Hopper"]
```
