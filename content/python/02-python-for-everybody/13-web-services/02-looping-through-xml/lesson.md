+++
id = "everybody.web-services.looping-through-xml"
title = "Looping through XML nodes"
minutes = 25
+++

# Looping through XML nodes

Real XML documents repeat the same kind of element many times: many stations, many loans, many sightings. You need a way to visit every one of them.

## findall gives you a list

`find` returns the first match. `findall` returns **all** matches as a list. Loop over the list like any other.

```python
import xml.etree.ElementTree as ET

text = """
<network>
  <station id="S1" status="open"><name>Mill Lane</name><bikes>4</bikes></station>
  <station id="S2" status="closed"><name>Quay Street</name><bikes>0</bikes></station>
  <station id="S3" status="open"><name>Hill Top</name><bikes>9</bikes></station>
</network>
"""
root = ET.fromstring(text)
stations = root.findall("station")
print(len(stations))        # 3
```

`findall("station")` looks at the **direct children** of `root` that are called `station`. It returns an empty list when there are none, so a loop over an empty result simply does nothing. That is much safer than `find`.

## Reading each node

Inside the loop, each item is an element, so everything from the last lesson still works.

```python
for st in root.findall("station"):
    name = st.find("name").text
    bikes = int(st.find("bikes").text)
    print(st.get("id"), name, bikes)
```

This prints:

```
S1 Mill Lane 4
S2 Quay Street 0
S3 Hill Top 9
```

## Collecting results

Often you build a total or a new list while looping. This is the same accumulator pattern you already know from lists and loops.

```python
total = 0
open_names = []
for st in root.findall("station"):
    total += int(st.find("bikes").text)
    if st.get("status") == "open":
        open_names.append(st.find("name").text)

print(total)        # 13
print(open_names)   # ['Mill Lane', 'Hill Top']
```

## Paths and levels

`findall` also accepts a path. `"station/name"` means "every `name` inside every `station`".

```python
names = [el.text for el in root.findall("station/name")]
print(names)   # ['Mill Lane', 'Quay Street', 'Hill Top']
```

To search at **any depth**, start the path with `.//`:

```python
print(len(root.findall(".//bikes")))   # 3
```

Think of `.//` as "anywhere below here".

## Nested loops

When elements nest, loop inside a loop. Imagine zones that contain stations:

```python
doc = ET.fromstring("""
<city>
  <zone name="North"><station>A</station><station>B</station></zone>
  <zone name="South"><station>C</station></zone>
</city>""")

for zone in doc.findall("zone"):
    for st in zone.findall("station"):
        print(zone.get("name"), st.text)
```

Output:

```
North A
North B
South C
```

## Walking the whole tree

Sometimes you just want everything. `root.iter()` walks every element in the tree, and `root.iter("bikes")` walks only those called `bikes`.

```python
for el in root.iter("bikes"):
    print(el.text)
```

## Debugging tip

If a loop finds nothing, print `len(root.findall(...))` and `root.tag`. Two usual causes: the path is one level off (the elements are deeper, so try `.//`), or you called `findall` on the wrong element. Also remember that `findall("station")` does not match the root itself.

## Common mistakes

- Using `find` when you need every match, and getting only the first.
- Forgetting to convert `.text` to a number before adding it up.
- Assuming a `findall` result is never empty. An empty list is fine to loop over, but `result[0]` would fail.
- Searching one level too shallow. Use `.//tag` when unsure how deep it is.
