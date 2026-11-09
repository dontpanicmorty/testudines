+++
id = "everybody.lists.lists-strings-functions"
title = "Lists with functions and strings"
minutes = 24
+++

# Lists with functions and strings

Lists and strings are close relatives. This lesson shows how to move between them, and how Python's built-in functions summarise lists.

## Built-in functions for lists

```python
nums = [3, 41, 12, 9]
print(len(nums))     # 4
print(sum(nums))     # 65
print(max(nums))     # 41
print(min(nums))     # 3
```

`sum` adds, `max` finds the largest, `min` the smallest. They work on lists of numbers. (`max` and `min` also work on strings, comparing alphabetically.)

### Averaging

An average is the total divided by the count:

```python
average = sum(nums) / len(nums)
print(average)       # 16.25
```

Careful with an empty list: `len` is 0 and dividing by zero raises an error. Check first:

```python
if len(nums) > 0:
    average = sum(nums) / len(nums)
```

## From a string to a list

`list` turns a string into a list of its characters:

```python
print(list("abc"))     # ['a', 'b', 'c']
```

`split` breaks a string into a list of words, which is usually more useful:

```python
words = "one two three".split()
print(words)           # ['one', 'two', 'three']
```

Without an argument it cuts at blanks. Give it a **delimiter** (the character that separates the pieces) to cut elsewhere.

```python
print("10;20;30".split(";"))    # ['10', '20', '30']
```

The pieces are strings, so convert them to do arithmetic:

```python
total = 0
for piece in "10;20;30".split(";"):
    total += int(piece)
print(total)   # 60
```

## From a list to a string

`join` is the reverse of `split`. Write the glue string, a dot, `join`, and give it the list of strings.

```python
print("-".join(["2025", "03", "14"]))   # 2025-03-14
print(" ".join(["a", "b"]))             # a b
print("".join(["a", "b"]))              # ab
```

All the elements must be strings, so numbers need `str()` first.

## Parsing lines

Combine these with file reading. Suppose each line of a made-up file looks like `ana,31,Leeds`:

```python
line = "ana,31,Leeds\n"
fields = line.rstrip().split(",")
name = fields[0]
age = int(fields[1])
city = fields[2]
```

You can even unpack the list in one go: `name, age, city = fields`, as long as the counts match.

Another common pattern: a line such as `From: sam@example.org`.

```python
line = "From: sam@example.org"
pieces = line.split()
address = pieces[1]
user, domain = address.split("@")
print(user, domain)    # sam example.org
```

This is a **double split**: split the line, then split one of the pieces again.

## Common mistakes

- Calling `max` or `sum` on a list that is empty.
- Forgetting to convert string pieces with `int()` before adding.
- Calling `join` on the list instead of the glue: it is `",".join(items)`, not `items.join(",")`.
- Trying to join numbers without converting them.
- Unpacking into the wrong number of variables.
