+++
id = "everybody.iteration.for-loops"
title = "Definite loops with for"
minutes = 20
+++

# Definite loops with for

A `while` loop repeats until a condition changes, so you often do not know in advance how many times it will run. When you *do* have a collection of things to work through, a `for` loop is simpler. It is called a **definite loop** because it runs exactly once for each item.

## Looping over a list

```python
planets = ["Mercury", "Venus", "Earth"]
for planet in planets:
    print("Hello,", planet)
```

This prints one greeting per planet. Here is how to read it:

- `planet` is the iteration variable. Python gives it the next item each time round.
- `planets` is the sequence being walked through.
- The indented block is the body, run once per item.

You choose the name of the iteration variable. Pick one that says what a single item is: `for name in names` reads like English.

## Looping over a string

A string is a sequence of characters, so `for` can walk through it too.

```python
for letter in "cat":
    print(letter)
```

This prints `c`, `a`, `t` on separate lines.

## Counting with range

To repeat something a set number of times, use `range`.

```python
for i in range(4):
    print(i)
```

This prints `0`, `1`, `2`, `3`. Notice that `range(4)` starts at 0 and stops *before* 4. Computers usually count from zero.

You can give `range` a start and an end, and even a step:

```python
for i in range(2, 6):      # 2, 3, 4, 5
    print(i)

for i in range(10, 0, -3): # 10, 7, 4, 1
    print(i)
```

## for or while?

- Use `for` when you have a collection, or a known number of repeats.
- Use `while` when you repeat until something happens and cannot say how many times in advance.

Both loops can use `break` and `continue`, exactly as in the last lesson.

```python
for n in range(1, 10):
    if n % 3 == 0:
        print("first multiple of 3:", n)
        break
```

## Changing the variable inside the loop

Python sets the iteration variable fresh at the top of every iteration. Changing it inside the body does not affect how many times the loop runs.

```python
for i in range(3):
    i = i * 10
    print(i)    # 0, 10, 20
```

## Common mistakes

- Forgetting the colon at the end of the `for` line.
- Forgetting to indent the body.
- Expecting `range(5)` to include 5. It stops at 4.
- Using the same name for the sequence and the iteration variable, for example `for word in word`.
- Looping with `for i in range(len(x))` when `for item in x` would be simpler and clearer.
