+++
id = "everybody.strings.comparing-and-methods"
title = "Comparing strings and string methods"
minutes = 24
+++

# Comparing strings and string methods

Strings come with a toolbox of ready-made actions. In this lesson you compare strings and learn the most useful tools.

## Comparing strings

The comparison operators work on strings.

```python
print("apple" == "apple")    # True
print("apple" == "Apple")    # False
print("apple" < "banana")    # True
```

`<` and `>` compare alphabetical order, but with a catch: every capital letter comes before every lower-case letter. So `"Zebra" < "apple"` is `True`. To compare fairly, convert both to the same case first, as in `a.lower() < b.lower()`.

## Methods

A **method** is a function that belongs to a value. You call it by writing the value, a dot, and the method name with brackets.

```python
word = "Hello"
print(word.upper())   # HELLO
print(word.lower())   # hello
```

Remember that strings cannot be changed. A method never changes the original; it returns a new string.

```python
word.upper()
print(word)           # still Hello
```

If you want to keep the result, store it: `word = word.upper()`.

You can see everything a string can do by typing `dir("")` in the Python prompt.

## Handy methods

**strip** removes spaces and other blank characters from both ends. It does not touch the middle.

```python
print("  hi there  ".strip())   # hi there
```

**startswith** and **endswith** answer `True` or `False`.

```python
print("report.txt".endswith(".txt"))   # True
print("report.txt".startswith("data")) # False
```

**replace** swaps every copy of one piece of text for another.

```python
print("a-b-c".replace("-", "+"))   # a+b+c
```

**count** says how many times a piece of text appears (no overlaps).

```python
print("banana".count("an"))   # 2
```

**find** gives the index where some text first appears, or `-1` if it is missing.

```python
print("banana".find("na"))   # 2
print("banana".find("x"))    # -1
```

You can tell `find` where to start looking with a second number: `"banana".find("a", 2)` returns `3`.

**split** chops a string into a list of pieces. With no argument it splits on any run of blanks.

```python
print("red green  blue".split())      # ['red', 'green', 'blue']
print("2025-03-14".split("-"))        # ['2025', '03', '14']
```

## Chaining

Because each method returns a string, you can attach another straight away.

```python
print("  Hello World ".strip().lower())   # hello world
```

## Common mistakes

- Writing `word.upper()` on its own line and expecting `word` to change.
- Forgetting the brackets: `word.upper` is not the same as `word.upper()`.
- Treating `-1` from `find` as a real position.
- Comparing `"Apple"` and `"apple"` and being surprised they differ.
- Using `in` when you need the position (use `find`).
