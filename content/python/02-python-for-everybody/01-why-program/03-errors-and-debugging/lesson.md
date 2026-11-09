+++
id = "everybody.why-program.errors-and-debugging"
title = "Mistakes, debugging and the road ahead"
minutes = 20
+++

# Mistakes, debugging and the road ahead

Every programmer makes mistakes, every day. What matters is how quickly you find and fix them. That skill is called **debugging**, and it gets easier with practice.

## Three kinds of error

Mistakes in a program come in three flavours. They behave quite differently, so it helps to know which one you are facing.

### Syntax errors

A **syntax error** means you broke the grammar rules, so Python cannot even understand the line. Python stops before running anything and points at the problem.

```python
print("Ready"
```

The closing bracket is missing, so Python reports a syntax error. These are the easiest errors to deal with, because Python tells you roughly where to look. The mistake is sometimes on the line just before the one it points at.

### Runtime errors

A **runtime error** (also called an **exception**) happens while the program is running. The line was grammatical, but something went wrong when Python tried to carry it out.

```python
print("Start")
print(10 / 0)
print("End")
```

`Start` is printed, then the program stops with a `ZeroDivisionError`. `End` never appears. Other common runtime errors are using a name that does not exist (`NameError`) and mixing incompatible values, like adding text to a number (`TypeError`).

### Logic and semantic errors

A **logic error** (or **semantic error**) is the sneakiest. The program runs without any complaint but gives the wrong answer, because what you wrote is not what you meant.

```python
total = 10 + 20 + 30
average = 10 + 20 + 30 / 3
print(average)
```

Python is not wrong here. Division happens before addition, so `30 / 3` is worked out first and the result is `40.0`, not `20.0`. The fix is brackets: `(10 + 20 + 30) / 3`.

Python cannot warn you about logic errors, because it only does what you ask. You find them by checking the output against what you expected.

## How to debug

Debugging is detective work. A routine that works well:

1. **Read the message.** Note the error name and the line number.
2. **Look at that line and the one above.** Check brackets, quotes and spelling.
3. **Predict, then run.** Say out loud what you expect each line to produce, then compare with what you really got.
4. **Print the middle.** Add a temporary `print` to see the value of something at a specific point.
5. **Shrink the problem.** Cut the code down until you have the smallest piece that still goes wrong.
6. **Change one thing at a time.** If you change five things, you will not know which fixed it.
7. **Take a break.** A short walk often finds the bug faster than another hour of staring.

A useful habit is to explain your code, line by line, to someone else, or even to a rubber duck on your desk. Explaining forces you to notice the line that does not say what you thought.

## Detecting errors in code

An exercise later will ask you to sort snippets into the three kinds. In a program, you can catch a runtime error rather than let it stop everything. Here is a peek at the idea; chapter 3 explains it fully:

```python
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")
```

The `try` block is attempted. If it fails with that error, the `except` block runs instead.

## The learning journey

Learning to program is like learning a language or a musical instrument. The first weeks feel awkward, then things start to click. A few tips for the road ahead:

- **Type the examples yourself** instead of copy and paste. Your fingers learn too.
- **Make small changes** to working code and see what changes.
- **Expect errors.** Red text is feedback, not a verdict on you.
- **Practise a little often.** Twenty minutes a day beats one long weekend.
- **Keep going when it is confusing.** Most ideas become clear only when you use them.

## Common mistakes

- **Fixing the symptom, not the cause.** If you patch the output so it looks right, the bug still lurks.
- **Ignoring the line number.** Python tells you where it noticed the problem, which is the best place to start.
- **Changing lots of things at once.**
- **Assuming the computer is wrong.** It almost never is; the instruction is.

## What to take away

1. Syntax errors break the grammar, runtime errors stop a running program, logic errors give wrong answers quietly.
2. Debug by reading the message, predicting, printing and shrinking the problem.
3. Change one thing at a time and keep going; everyone gets stuck.
