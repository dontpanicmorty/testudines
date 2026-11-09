+++
id = "everybody.web-services.json-data"
title = "JSON: objects and arrays"
minutes = 25
+++

# JSON: objects and arrays

XML works, but it is wordy. Most modern services send **JSON** instead (short for JavaScript Object Notation). Despite the name, every language can read it, and it looks very familiar to a Python programmer.

## JSON is Python's cousin

```json
{
  "member": "Ines",
  "active": true,
  "books": ["Tide Tables", "Moss and Stone"],
  "address": {"town": "Larkfield", "zip": null}
}
```

JSON has only a few building blocks, and each has a Python partner:

| JSON | Python |
|------|--------|
| object `{...}` | dictionary (`dict`) |
| array `[...]` | list |
| string `"..."` | string |
| number | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Two small rules differ from Python. JSON strings must use **double quotes**, and `true`, `false` and `null` are written in lowercase.

## Parsing with json.loads

The `json` module is part of the standard library. `json.loads(text)` ("load string") turns JSON text into Python values.

```python
import json

text = '{"member": "Ines", "active": true, "books": ["Tide Tables", "Moss and Stone"]}'
data = json.loads(text)

print(type(data))          # <class 'dict'>
print(data["member"])      # Ines
print(data["active"])      # True
print(data["books"][1])    # Moss and Stone
```

After parsing there is no JSON left, just ordinary dictionaries and lists. Everything you know about them applies.

Unlike XML, numbers arrive as numbers: `{"bikes": 12}` gives you the integer `12`, not the string `"12"`.

## Nested access

JSON often nests deeply. Read it one step at a time, from the outside in.

```python
data = json.loads('{"result": {"items": [{"id": 1, "tags": ["a", "b"]}, {"id": 2, "tags": []}]}}')

items = data["result"]["items"]
print(items[0]["id"])         # 1
print(items[0]["tags"][1])    # b
print(len(items[1]["tags"]))  # 0
```

A handy trick: print the pieces as you go. `print(data["result"])` shows what is one level down, so you never have to guess.

## Missing keys

A missing key raises `KeyError`. Use `.get` when a key might be absent:

```python
print(data["result"].get("count", 0))    # 0
```

For a deep path, chain carefully. This function walks a list of keys and gives up with a default:

```python
def dig(value, keys, default=None):
    for key in keys:
        try:
            value = value[key]
        except (KeyError, IndexError, TypeError):
            return default
    return value

print(dig(data, ["result", "items", 0, "id"]))      # 1
print(dig(data, ["result", "items", 5, "id"], -1))  # -1
```

## Going the other way: json.dumps

`json.dumps(value)` ("dump string") turns Python values into JSON text. That is serialization.

```python
record = {"member": "Ines", "books": 2, "late": False}
print(json.dumps(record))
print(json.dumps(record, indent=2, sort_keys=True))
```

`indent=2` makes the text readable, and `sort_keys=True` puts keys in a steady order. Only plain data can be serialized: a `set` or a custom object will raise `TypeError`.

## When parsing fails

Broken JSON raises `json.JSONDecodeError`. The usual causes are single quotes, a trailing comma, or an empty string.

```python
try:
    json.loads("{'a': 1}")
except json.JSONDecodeError as err:
    print("not valid json:", err)
```

## Common mistakes

- Using single quotes in JSON text.
- Confusing `loads` (from a string) with `load` (from an open file).
- Indexing a list with a string key, or a dict with a number, when walking nested data.
- Forgetting that JSON arrays become lists, so you loop over them rather than looking up keys.
