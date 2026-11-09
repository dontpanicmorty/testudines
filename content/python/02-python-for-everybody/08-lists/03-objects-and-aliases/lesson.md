+++
id = "everybody.lists.objects-and-aliases"
title = "Objects, aliases and list arguments"
minutes = 25
+++

# Objects, aliases and list arguments

This lesson explains a surprising feature of lists: two names can point at the very same list. Understanding it will save you from some of the most puzzling bugs.

## Values and objects

When you write `a = "banana"`, Python creates a string **object** in memory and makes the name `a` refer to it. Think of a name as a sticky label attached to an object.

```python
a = "banana"
b = "banana"
```

Do `a` and `b` refer to the *same* object, or to two objects that look alike? Python gives you two different questions:

- `a == b` asks: do they have the same *value*?
- `a is b` asks: are they the *same object*?

For lists the difference is clear:

```python
x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)   # True  (same contents)
print(x is y)   # False (two separate lists)
```

Use `==` to compare contents. Use `is` mainly for checking `is None`.

## Aliasing

If you assign one name to another, you do not copy the list. Both names now label the same object. This is called an **alias**.

```python
x = [1, 2, 3]
z = x
print(x is z)   # True
z[0] = 99
print(x)        # [99, 2, 3]
```

Changing the list through one name changes it for the other, because there is only one list. With immutable things such as strings and numbers, aliasing is harmless since they cannot change. With lists, be careful.

To get an independent copy, make one on purpose:

```python
copy = x[:]            # a slice of everything
copy2 = list(x)        # another way
copy[0] = 0
print(x)               # unchanged by that
```

These copies are one level deep. A list inside a list is still shared.

## List arguments

When you pass a list to a function, the parameter becomes an alias of the list you passed. So a function can change your list.

```python
def add_end(items):
    items.append("end")

stuff = ["a"]
add_end(stuff)
print(stuff)    # ['a', 'end']
```

The function returned nothing, yet the caller's list changed. This is sometimes exactly what you want, and sometimes a nasty surprise.

Compare it with a function that creates a new list and leaves the original alone:

```python
def with_end(items):
    return items + ["end"]    # + builds a brand new list

stuff = ["a"]
longer = with_end(stuff)
print(stuff)     # ['a']
print(longer)    # ['a', 'end']
```

Watch the difference between these two lines inside a function:

```python
items.append(1)       # modifies the caller's list
items = items + [1]   # rebinds the local name; caller's list untouched
```

Good habit: make it clear in the function name or comment whether it changes its argument or returns a new list. A function that modifies a list in place usually returns `None`; one that builds a new list returns it.

## Debugging list problems

- Print the list before and after each suspicious step.
- When two variables change together unexpectedly, check `a is b`.
- If a value is `None` where a list should be, look for `x = x.sort()` or `x = x.append(...)`.
- Remember that `[[0] * 3] * 2` makes two aliases of the same inner list. Build such tables with a loop.

## Common mistakes

- Thinking `b = a` makes a copy.
- Using `is` where you meant `==`.
- Changing a list passed to your function when the caller did not expect it.
- Returning the result of `append` or `sort`, which is `None`.
