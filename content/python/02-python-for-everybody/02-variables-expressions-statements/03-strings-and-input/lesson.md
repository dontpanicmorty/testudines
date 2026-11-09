+++
id = "everybody.variables-expressions-statements.strings-and-input"
title = "Strings, input and conversions"
minutes = 25
+++

# Strings, input and conversions

So far our programs have used fixed values. Real programs ask questions and use the answers. This lesson covers working with text and getting information from the person using your program.

## Text and the `+` and `*` operators

Strings (text) have their own versions of some operators. The `+` operator **joins** two strings, which is called **concatenation**:

```python
first = "tea"
second = "pot"
print(first + second)
print(first + " " + second)
```

This shows `teapot`, then `tea pot`. Notice Python does not add spaces for you; you add the `" "` yourself.

The `*` operator **repeats** a string:

```python
print("ha" * 3)
print("-" * 20)
```

This shows `hahaha`, then a line of twenty dashes. It is a handy way to draw a line.

You cannot mix text and numbers with `+`. This fails with a `TypeError`:

```python
print("Cups: " + 3)
```

Python does not know whether you want to add or to join. We fix this shortly.

## Converting between types

The functions `int()`, `float()` and `str()` convert a value to another type.

```python
print(int("12") + 1)       # 13
print(float("2.5") * 2)    # 5.0
print("Cups: " + str(3))   # Cups: 3
print(int(7.9))            # 7, the fraction is chopped off
```

The first line turns the text `"12"` into the number `12` before adding. The third turns the number `3` into text so it can be joined. `int(7.9)` does not round; it simply drops what is after the point.

If the text cannot be turned into a number, Python gives a `ValueError`:

```python
int("twelve")
int("3.5")
```

Both fail. `"3.5"` is not a whole number, though `float("3.5")` is fine.

## Asking the user: `input`

The built-in `input` function shows a message, waits for the person to type something and press Enter, and hands back what they typed:

```python
name = input("What is your name? ")
print("Nice to meet you, " + name)
```

The text inside `input(...)` is the **prompt**. Whatever the user types is stored in `name`.

The key point: **`input` always gives back a string**, even when the user types digits. To calculate with the answer, convert it:

```python
age_text = input("How old are you? ")
age = int(age_text)
print("Next year you will be", age + 1)
```

Often these two steps are joined in one line: `age = int(input("How old are you? "))`. The inside part runs first, then `int` converts the result.

(`print` can take several values separated by commas and puts spaces between them, which also avoids the text-plus-number problem.)

## Testing code that calls `input`

The exercises in this course are marked by an automatic program, which cannot type answers. So an exercise that needs `input` is written as a function. The marking code pretends to be the person typing. All you do is write the function the normal way, calling `input` once for each question. If the function's name is `ask_age`, it might look like this:

```python
def ask_age():
    reply = input("Age? ")
    return int(reply)
```

## Looking inside strings

A string is a sequence of characters, and each has a position, counted from **zero**. Square brackets pick one out, and `len` gives the length:

```python
word = "banana"
print(word[0])      # b, the first
print(word[1])      # a
print(word[-1])     # a, the last
print(len(word))    # 6
```

We will explore strings much further in chapter 6.

## Comments

A **comment** starts with `#`. Python ignores everything from the `#` to the end of the line. Comments are notes for people:

```python
# Convert minutes to hours
minutes = 90
hours = minutes / 60    # a float, so 1.5
```

Good comments explain *why* you did something, not what the line already says plainly.

## Common mistakes

- **Forgetting that `input` returns text.** `input("n? ") + 1` fails; use `int(input("n? ")) + 1`.
- **Adding text and a number.** Convert the number with `str()`, or use commas in `print`.
- **Converting words to numbers.** `int("ten")` is a `ValueError`.
- **Counting from 1.** The first character is at position 0.
- **Forgetting to add spaces** when joining strings with `+`.

## What to take away

1. `+` joins strings and `*` repeats them; neither mixes text and numbers.
2. `int()`, `float()` and `str()` convert between types.
3. `input(prompt)` always returns a string; convert it before doing arithmetic.
4. `#` starts a comment, a note ignored by Python.
