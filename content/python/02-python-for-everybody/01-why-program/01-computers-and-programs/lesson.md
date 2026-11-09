+++
id = "everybody.why-program.computers-and-programs"
title = "Why program, and what is a computer?"
minutes = 20
+++

# Why program, and what is a computer?

You use software every day: a phone, a map, a shop checkout. All of it was written by people who typed instructions for a computer. Learning to program means learning to write those instructions yourself.

You do not need to be a mathematician or an "IT person". You need patience, curiosity and a willingness to try things and see what happens. This course starts from zero.

## Why learn to program?

Here are a few honest reasons.

- **Boring jobs get automated.** Renaming 400 files, tidying a spreadsheet or collecting numbers from a web page can take a program a few seconds.
- **You can make your own tools.** If no app does exactly what you want, you can build one.
- **You understand the world better.** Once you know how a program thinks, the technology around you stops feeling like magic.

Think of a program as a recipe. A computer is a very fast, very literal cook: it follows each step exactly, and it never guesses what you meant.

## The parts of a computer

A computer is made of a few parts that each do one job.

- **Central processing unit (CPU).** The "brain". It does the actual work, following instructions one after another, billions of times per second. It does not remember anything for long.
- **Main memory.** Fast storage that holds whatever the computer is working on *right now*. When the power goes off, main memory is wiped.
- **Secondary memory.** Slower but permanent storage, such as a hard drive or a phone's flash storage. Your photos and saved files live here.
- **Input devices.** Ways to get information in: keyboard, mouse, touch screen, microphone.
- **Output devices.** Ways to get information out: screen, speakers, printer.
- **Network.** A connection to other computers, for example through wifi. It lets your computer fetch and send data.

When you open a document, the computer copies it from secondary memory into main memory so the CPU can work on it quickly. When you press save, it copies it back.

> Memory sizes are counted in bytes. A kilobyte is about a thousand bytes, a megabyte about a million, and a gigabyte about a billion. A typical phone photo is a few megabytes.

## What is programming?

A **program** is a list of instructions written so that a computer can follow them. Writing programs is called **programming**, and the person doing it is a **programmer**.

Computers do not understand English. They understand a tiny set of very simple operations: add two numbers, compare two numbers, move data from here to there. A **programming language** lets us write bigger ideas in a readable form, and then turns them into those simple operations. In this course we use a language called **Python**.

Python was designed to be readable. Here is a complete Python instruction. It tells the computer to display some text:

```python
print("Good morning")
```

`print` is a command that shows something on the screen. The text between the quotation marks is what gets shown. We will take this apart properly in the next lesson.

## How the exercises work

Each exercise asks you to finish a small **function**. A function is a named piece of code that takes some values in and gives an answer back. Do not worry about the details yet; chapter 4 covers them. For now, the exercise gives you a starting point like this:

```python
def double(number):
    # TODO: replace the next line
    return 0
```

The word `return` hands the answer back. Here you would change `return 0` to `return number * 2`. The checks then call your function with several test values and compare the answers.

## Common mistakes

- **Thinking the computer will "figure out" what you meant.** It follows your words literally. If you ask for the wrong thing, you get the wrong thing.
- **Mixing up the two kinds of memory.** If you lose work when the power goes out, it was only in main memory. Save it to secondary memory.
- **Believing you have to be a genius.** Programmers make mistakes all day and fix them. That is the job.
- **Typing quotation marks the wrong way.** Use straight quotes like `"` in code. Curly quotes copied from a word processor will not work.

## What to take away

1. A program is a list of instructions; Python is the language we will write them in.
2. The CPU works, main memory is fast and temporary, secondary memory is permanent.
3. Input devices bring information in, output devices show it, the network connects computers.
4. Exercises ask you to complete a function and hand back a value with `return`.
