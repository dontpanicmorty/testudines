A library feed lists its branches like this:

```xml
<library>
  <branch><name>Central</name></branch>
  <branch><name>Riverside</name></branch>
</library>
```

Write `branch_names(xml_text)` that returns the branch names as a list of strings, in document order. If there are no branches, return an empty list.
