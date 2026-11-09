+++
id = "everybody.dictionaries.what-is-a-dictionary"
title = "What is a dictionary?"
minutes = 25
+++

# What is a dictionary?

So far you have met one way to hold many values: the **list**. A list keeps things in order and you find an item by its position, like `fruit[0]`. That works well until you ask a different question: "what is Maya's phone number?" You do not want to remember that Maya is at position 7. You want to look her up by name.

A **dictionary** does exactly that. It stores **key/value pairs**. The **key** is the label you search with. The **value** is the thing you get back.

## Making a dictionary

Use curly braces. Each pair is `key: value`, and pairs are separated by commas.

```python
phones = {"Maya": "555-0101", "Tomas": "555-0142"}
print(phones)
```

An empty dictionary is just `{}`. You can also build one step by step.

```python
stock = {}
stock["apples"] = 12
stock["pears"] = 4
print(stock)
```

The line `stock["apples"] = 12` means: "under the key `"apples"`, store the value `12`". If the key is already there, the old value is replaced. If it is not, a new pair is added.

## Looking things up

Put the key in square brackets.

```python
print(phones["Maya"])      # 555-0101
```

Keys are matched exactly. `"maya"` with a small `m` is a different key from `"Maya"`.

If the key does not exist, Python stops with a `KeyError`.

```python
print(phones["Priya"])     # KeyError: 'Priya'
```

## Asking "is it there?" with `in`

The word `in` works on dictionaries too. It checks the **keys**.

```python
print("Maya" in phones)    # True
print("Priya" in phones)   # False

if "Priya" in phones:
    print(phones["Priya"])
else:
    print("No such contact")
```

Checking first avoids the `KeyError`. There is also a shortcut called `.get()` that takes a fallback value, and you will use it a lot in the next lesson:

```python
print(phones.get("Priya", "unknown"))   # unknown
```

## Keys, values and size

`len()` tells you how many pairs there are. The `.keys()` and `.values()` methods give you the keys or the values on their own.

```python
print(len(phones))               # 2
print(list(phones.keys()))       # ['Maya', 'Tomas']
print(list(phones.values()))     # ['555-0101', '555-0142']
```

We wrap them in `list(...)` here only so they print nicely. You can loop over them directly.

Using `in` on `.values()` checks the values instead of the keys:

```python
print("555-0142" in phones.values())   # True
```

This is slower than checking keys, because Python has to walk through every value. Checking a key is nearly instant even in a huge dictionary. That speed is the whole reason dictionaries exist.

## Rules for keys

- Keys must be unique. Writing the same key twice keeps only the last value.
- Keys must be a kind of value that can never change: strings, numbers and (later) tuples are fine. A list cannot be a key.
- Values can be anything: numbers, strings, lists, even other dictionaries.

```python
scores = {"Ana": [90, 85], "Ben": [70]}
scores["Ben"].append(88)
print(scores)     # {'Ana': [90, 85], 'Ben': [70, 88]}
```

## Debugging tip: look at small pieces

When a dictionary misbehaves, print it. Print `len()`, print one key you expect, print `"key" in d`. A dictionary with 3 entries is easy to check by eye; do that before you try a big one.

## Common mistakes

- Using `d[key]` for a key that may be missing. Check with `in` or use `.get()`.
- Forgetting that `in` checks keys, not values.
- Mixing up capital letters: `"Maya"` and `"maya"` are different keys.
- Using square brackets to build one: `["a": 1]` is an error. Dictionaries use curly braces.
