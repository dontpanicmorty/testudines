+++
id = "everybody.strings.strings-as-sequences"
title = "A string is a sequence"
minutes = 22
+++

# A string is a sequence

A **string** is text: a row of characters in quotes. What makes strings powerful is that Python treats them as a **sequence**, an ordered row of items you can pick from by position.

## Indexing

Each character has a position number called an **index**. Counting starts at 0.

```python
word = "banana"
print(word[0])   # b
print(word[1])   # a
print(word[5])   # a
```

The square brackets pick out one character. Negative numbers count from the end:

```python
print(word[-1])  # a  (the last one)
print(word[-2])  # n
```

Asking for a position that does not exist, like `word[6]`, stops the program with an `IndexError`.

## Length

The built-in `len` tells you how many characters a string holds.

```python
print(len("banana"))   # 6
```

The last valid index is always `len(word) - 1`.

## Walking through a string

You can use a `for` loop to visit every character:

```python
for ch in "hey":
    print(ch)
```

Or a `while` loop with your own index, when you need the position as well:

```python
word = "hey"
i = 0
while i < len(word):
    print(i, word[i])
    i += 1
```

## Slices

A **slice** cuts out a piece of a string. Write two numbers with a colon between them: `text[start:stop]`. It includes `start` but stops just before `stop`.

```python
s = "Monty Python"
print(s[0:5])    # Monty
print(s[6:12])   # Python
```

If you leave out the first number the slice starts at the beginning. If you leave out the second, it runs to the end.

```python
print(s[:5])     # Monty
print(s[6:])     # Python
print(s[:])      # Monty Python  (a full copy)
```

Slices never cause an `IndexError`. A slice that goes too far just stops at the end.

## Strings cannot be changed

Strings are **immutable**: once made, a string cannot be altered in place.

```python
s = "hello"
s[0] = "J"     # TypeError!
```

Instead, build a new string and give it a name:

```python
s = "J" + s[1:]
print(s)       # Jello
```

## Looping and counting

Combine a loop with the counter pattern to count a certain letter:

```python
count = 0
for ch in "mississippi":
    if ch == "s":
        count += 1
print(count)   # 4
```

## The in operator

`in` asks whether one string appears inside another. The answer is `True` or `False`.

```python
print("an" in "banana")   # True
print("z" in "banana")    # False
```

## Common mistakes

- Thinking the first character is at index 1. It is at index 0.
- Using `word[len(word)]`, which is one past the end.
- Expecting `s[0:3]` to include the character at index 3.
- Trying to assign to a position in a string.
- Forgetting that upper and lower case letters are different: `"A" in "banana"` is `False`.
