+++
id = "everybody.lists.list-basics"
title = "Lists: a changeable sequence"
minutes = 24
+++

# Lists: a changeable sequence

A string holds a sequence of characters. A **list** holds a sequence of anything: numbers, strings, even other lists. It is written with square brackets and commas.

```python
scores = [90, 72, 85]
names = ["Ana", "Bo", "Cy"]
mixed = ["pen", 4, 2.5, True]
empty = []
```

The things inside a list are called its **elements** (or items).

## Indexing and length

Just like strings, lists are sequences. Positions start at 0 and negative numbers count from the end.

```python
print(names[0])      # Ana
print(names[-1])     # Cy
print(len(names))    # 3
```

## Lists can be changed

Unlike strings, lists are **mutable**: you can change an element in place.

```python
scores[1] = 75
print(scores)    # [90, 75, 85]
```

## Traversing a list

Use `for` to visit each element:

```python
for name in names:
    print(name)
```

If you need to change elements, you need the positions, so use `range(len(...))`:

```python
for i in range(len(scores)):
    scores[i] = scores[i] + 5
```

## Joining and repeating

`+` glues two lists into a new one. `*` repeats a list.

```python
print([1, 2] + [3])    # [1, 2, 3]
print([0] * 4)         # [0, 0, 0, 0]
```

## Slices

Slices work exactly as they do on strings, and give a new list.

```python
letters = ["a", "b", "c", "d", "e"]
print(letters[1:3])    # ['b', 'c']
print(letters[:2])     # ['a', 'b']
print(letters[3:])     # ['d', 'e']
```

## List methods

Methods change a list in place and usually return `None`.

```python
bag = ["pen"]
bag.append("cup")         # add one element at the end
bag.extend(["ink", "tape"])   # add several at the end
print(bag)                # ['pen', 'cup', 'ink', 'tape']
```

`append` adds one thing. If you append a list, you get a list inside the list. `extend` adds each element separately.

```python
nums = [5, 2, 9]
nums.sort()               # puts them in order
print(nums)               # [2, 5, 9]
```

A common trap: `nums = nums.sort()` sets `nums` to `None`, because `sort` changes the list and returns nothing.

## Removing elements

```python
items = ["a", "b", "c", "d"]
last = items.pop()        # removes and returns "d"
second = items.pop(1)     # removes and returns "b"
items.remove("a")         # removes the first "a" by value
print(items)              # ['c']
```

`pop` works by position. `remove` works by value, and raises an error if the value is absent. The `del` statement removes by position, or a whole slice:

```python
nums = [10, 20, 30, 40, 50]
del nums[0]
del nums[1:3]
print(nums)   # [20, 50]
```

## Common mistakes

- Writing `x = x.append(3)`, which makes `x` equal to `None`.
- Confusing `append` with `extend`.
- Calling `remove` with a value that is not in the list.
- Going past the end: with 3 elements, `items[3]` is an error.
- Changing a list while looping over it, which skips elements.
