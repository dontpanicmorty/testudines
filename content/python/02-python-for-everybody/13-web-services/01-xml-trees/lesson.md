+++
id = "everybody.web-services.xml-trees"
title = "Sharing data: XML and trees"
minutes = 25
+++

# Sharing data: XML and trees

Your programs do not live alone. One program collects bike-share readings, another draws charts, and a third lives on a different computer. To work together they have to hand data to each other, and that hand-off needs an agreed format.

## Serialization in plain words

Inside your program, data is a dictionary, a list, a number. You cannot paste a Python dictionary into an email or send it down a network cable. First you turn it into **text** that follows agreed rules. Turning data into text is called **serialization**. Turning text back into data is called **parsing** (or deserialization).

Two formats do most of the work on the web: **XML** and **JSON**. This lesson covers XML. The next one covers JSON.

## What XML looks like

XML marks up data with named **tags**. A piece of data is wrapped between an opening tag and a closing tag. Together they are an **element**.

```xml
<station id="S7" status="open">
  <name>Harbour Gate</name>
  <bikes unit="count">12</bikes>
</station>
```

Here is what each part means:

- `<station> ... </station>` is an element. It contains other elements.
- `id="S7"` and `status="open"` are **attributes**: little labelled facts stored inside the opening tag.
- `Harbour Gate` and `12` are **text**: the content between tags.

Elements inside elements form a **tree**. The outermost element is the **root**. Elements inside it are its **children**. Here `station` is the root, and `name` and `bikes` are its children.

## Parsing with ElementTree

Python's standard library includes `xml.etree.ElementTree`. It reads XML text and gives you the tree as objects.

```python
import xml.etree.ElementTree as ET

text = """<station id="S7" status="open">
  <name>Harbour Gate</name>
  <bikes unit="count">12</bikes>
</station>"""

root = ET.fromstring(text)
print(root.tag)          # station
```

`ET.fromstring(text)` reads a string and returns the root element. Every element has a `.tag`, which is its name.

## find, text and get

To reach a child, call `find` with the child's tag name. To read the text inside an element use `.text`. To read an attribute use `.get`.

```python
name = root.find("name")
print(name.text)                 # Harbour Gate

bikes = root.find("bikes")
print(bikes.text)                # 12  (a string!)
print(int(bikes.text))           # 12  (a number)
print(bikes.get("unit"))         # count
print(root.get("status"))        # open
```

Notice that `.text` is always a **string**, even when it looks like a number. Convert it with `int()` or `float()` before doing sums.

`get` on a missing attribute returns `None`. You can give a fallback:

```python
print(root.get("zone"))              # None
print(root.get("zone", "unknown"))   # unknown
```

## When the element is missing

`find` returns `None` when no child has that tag. Then `.text` on it crashes, because `None` has no `.text`.

```python
colour = root.find("colour")
print(colour)            # None
# print(colour.text)     # AttributeError!

if colour is not None:
    print(colour.text)
else:
    print("no colour listed")
```

Always check `is not None` when an element might be absent. Do not write `if colour:`, because an element with no children can count as false even when it exists.

An element can also exist but be empty, like `<name></name>`. Then `.text` is `None` too.

## Going deeper

`find` accepts a path with slashes to walk down several levels at once:

```python
doc = ET.fromstring("<zone><area><label>North</label></area></zone>")
print(doc.find("area/label").text)    # North
```

## Debugging tip

When XML will not parse, `ET.fromstring` raises `ET.ParseError`. Common causes are a missing closing tag, a stray `&` character, or text before the first tag. Read the error: it gives a line and column.

```python
try:
    ET.fromstring("<a><b></a>")
except ET.ParseError as err:
    print("bad xml:", err)
```

## Common mistakes

- Forgetting that `.text` is a string and adding it to a number.
- Calling `.text` on the result of `find` without checking for `None`.
- Mixing up text (between tags) and attributes (inside the tag): use `.text` for one and `.get()` for the other.
- Writing tags in different cases: `<Name>` and `<name>` are different tags.
