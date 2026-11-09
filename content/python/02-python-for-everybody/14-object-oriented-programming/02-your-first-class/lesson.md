+++
id = "everybody.object-oriented-programming.your-first-class"
title = "Your first class"
minutes = 30
+++

# Your first class

Python gives you strings, lists and dictionaries. A **class** lets you invent your own kind of object. A class is a blueprint, and each object built from it is called an **instance**.

## A very small class

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
        self.page = 0

    def read(self, count):
        self.page = min(self.pages, self.page + count)

    def pages_left(self):
        return self.pages - self.page
```

That is a lot of new words, so here they are one at a time.

- `class Book:` starts the blueprint. Class names usually start with a capital letter.
- `def __init__(self, ...)` is a special method called the **constructor**. Python runs it automatically right after a new object is created. Its job is to set up the object's starting data.
- `self` is the object being worked on. It is always the first parameter of a method. When you write `self.title = title`, you store the value on this particular object.
- Names stored on `self` are **attributes**: the object's own data.
- `read` and `pages_left` are ordinary **methods**. They have `self` first so they can reach the object's attributes.

## Making and using instances

Call the class like a function to build an instance:

```python
tide = Book("Tide Tables", 200)
print(tide.title)        # Tide Tables
print(tide.page)         # 0
tide.read(30)
print(tide.pages_left()) # 170
```

You never pass `self` yourself. Python fills it in: `tide.read(30)` runs `read` with `self` set to `tide` and `count` set to `30`.

## Classes are types

Once `Book` exists, it is a type just like `str` or `list`:

```python
print(type(tide))                  # <class '__main__.Book'>
print(isinstance(tide, Book))      # True
print(isinstance(tide, str))       # False
```

## Many instances, separate data

Each instance has its own attributes. Changing one does not affect the others.

```python
moss = Book("Moss and Stone", 90)
moss.read(90)
print(moss.pages_left())   # 0
print(tide.pages_left())   # 170
```

The class holds the shared blueprint. The instance holds the personal data.

## Printing your objects

If you print a Book, Python shows something unhelpful like `<__main__.Book object at 0x...>`. Add a `__str__` method to say how the object should look as text:

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
        self.page = 0

    def __str__(self):
        return f"{self.title} ({self.page}/{self.pages})"

print(Book("Reed Songs", 50))   # Reed Songs (0/50)
```

`__str__` must **return** a string rather than print one.

## Objects that hold other objects

Attributes can be any value, including lists of other objects. This is how you assemble bigger designs:

```python
class Shelf:
    def __init__(self):
        self.books = []

    def add(self, book):
        self.books.append(book)

    def unread(self):
        return [b.title for b in self.books if b.page == 0]
```

A `Shelf` has a list of `Book` instances, and its methods use the books' own attributes.

## Debugging tip

Two error messages tell you the exact slip:

- `TypeError: read() takes 2 positional arguments but 3 were given` usually means you forgot `self` in the method definition.
- `AttributeError: 'Book' object has no attribute 'pages'` means you used a name that `__init__` never set, or you misspelled it. Look for `self.` typos.

## Common mistakes

- Leaving out `self` in the method's parameters, or forgetting `self.` when reading an attribute (`title` instead of `self.title`).
- Writing `def init` instead of `def __init__` (two underscores on each side).
- Printing inside `__str__` instead of returning.
- Using one shared list as a default value for every object (more on that in the next lesson).
