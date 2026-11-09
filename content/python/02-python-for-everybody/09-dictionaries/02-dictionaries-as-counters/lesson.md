+++
id = "everybody.dictionaries.dictionaries-as-counters"
title = "Dictionaries as counters"
minutes = 25
+++

# Dictionaries as counters

One of the most common jobs in programming is counting how many times each thing appears. How many times does each word show up in an essay? How many visits did each page get? How many orders did each customer place?

A dictionary is perfect for this. Use the thing you are counting as the **key** and the running total as the **value**.

## Counting by hand

Suppose we want to count the colors in a list.

```python
colors = ["red", "blue", "red", "green", "blue", "red"]
```

The idea: walk through the list. For each color, if we have not seen it, start its count at 1. If we have, add 1.

```python
counts = {}
for color in colors:
    if color not in counts:
        counts[color] = 1
    else:
        counts[color] = counts[color] + 1
print(counts)    # {'red': 3, 'blue': 2, 'green': 1}
```

Read the loop slowly. `counts` starts empty. The first `"red"` is not a key yet, so we create it with value `1`. The second `"red"` is a key, so we replace its value with the old value plus one.

This works but it is wordy. Python has a shorter way.

## The `.get()` method with a default

`d.get(key, default)` returns the value for `key` if it exists, and `default` if it does not. It never raises a `KeyError`.

```python
counts = {"red": 2}
print(counts.get("red", 0))     # 2
print(counts.get("pink", 0))    # 0
```

If we use `0` as the default, a missing color counts as "seen zero times so far". Adding one to that gives exactly what we want, and the whole `if` / `else` collapses into one line:

```python
counts = {}
for color in colors:
    counts[color] = counts.get(color, 0) + 1
print(counts)
```

This line is the single most useful dictionary pattern. Say it aloud: "the new count is the old count (or zero) plus one."

## Counting other things

The same pattern counts anything. Here we count how many times each letter appears in a word.

```python
word = "banana"
letters = {}
for ch in word:
    letters[ch] = letters.get(ch, 0) + 1
print(letters)    # {'b': 1, 'a': 3, 'n': 2}
```

And here we add up an amount per key instead of adding one:

```python
sales = [("tea", 3), ("milk", 2), ("tea", 4)]
totals = {}
for item, qty in sales:
    totals[item] = totals.get(item, 0) + qty
print(totals)     # {'tea': 7, 'milk': 2}
```

(The `for item, qty in sales` line takes each small pair apart into two names. You will study this properly in the next chapter.)

## Other defaults

A default does not have to be zero. When each value is a list, the default is an empty list.

```python
pets = [("Ana", "cat"), ("Ben", "dog"), ("Ana", "fish")]
owned = {}
for owner, pet in pets:
    owned[owner] = owned.get(owner, []) + [pet]
print(owned)      # {'Ana': ['cat', 'fish'], 'Ben': ['dog']}
```

## Debugging with small inputs

If your counts look wrong, shrink the problem. Try a list of three items you can count in your head, and print the dictionary after each step.

```python
for color in ["red", "red", "blue"]:
    counts[color] = counts.get(color, 0) + 1
    print(color, counts)
```

Seeing the dictionary grow one step at a time shows you exactly where it goes wrong. Another quick **sanity check**: the counts should add up to the number of items you looked at. `sum(counts.values())` must equal `len(colors)`.

## Common mistakes

- Writing `counts[key] += 1` for a key that does not exist yet. That raises a `KeyError`. Use `.get(key, 0)` or check with `in`.
- Putting `counts = {}` inside the loop. The dictionary then restarts empty on every pass and always ends with one entry.
- Choosing the wrong default, such as `""` instead of `0`.
- Forgetting that `"Red"` and `"red"` count separately unless you change the case first.
