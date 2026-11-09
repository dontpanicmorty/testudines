+++
id = "everybody.object-oriented-programming.lifecycle-and-instances"
title = "Lifecycle and many instances"
minutes = 25
+++

# Lifecycle and many instances

Every object has a life: it is **created**, it is **used**, and eventually it is **thrown away**. Knowing the stages helps you predict what your program will do.

## Birth: the constructor

Creating an instance calls `__init__`. That is the constructor, and it is where you set up attributes.

```python
class Bike:
    def __init__(self, bike_id):
        print("building bike", bike_id)
        self.bike_id = bike_id
        self.rented = False

a = Bike("B1")      # building bike B1
b = Bike("B2")      # building bike B2
```

Each call to `Bike(...)` makes a brand-new instance with its own attributes. That is what "multiple instances" means: one blueprint, many independent objects.

## Life: using the object

```python
a.rented = True
print(a.rented, b.rented)    # True False
```

You can also read and change attributes from outside, but it is usually tidier to give the class methods for that, so the rules live in one place:

```python
class Bike:
    def __init__(self, bike_id):
        self.bike_id = bike_id
        self.rented = False

    def rent(self):
        if self.rented:
            return False
        self.rented = True
        return True
```

## Death: the destructor

When nothing refers to an object any more, Python frees it. Just before that, it runs a method called `__del__`, known as the **destructor**, if the class has one.

```python
class Session:
    def __init__(self, name):
        self.name = name
        print("open", name)

    def __del__(self):
        print("close", self.name)

s = Session("alpha")    # open alpha
del s                   # close alpha
```

`del s` removes the name `s`. With no names left, the object is discarded and its destructor runs.

A word of caution: you rarely need `__del__`. When exactly it runs is Python's decision (especially if objects refer to each other, or the program is ending), so do not depend on it for important work. For cleanup that must happen, use an explicit `close()` method, or a `with` block like the one you use for files. Think of `__del__` as a last chance, not a plan.

## The shared-default trap

This one catches nearly everyone. A default value in a function header is created **once**, when the function is defined. If it is a list, every call shares it:

```python
class Playlist:
    def __init__(self, name, tracks=[]):    # DON'T
        self.name = name
        self.tracks = tracks

p1 = Playlist("morning")
p2 = Playlist("evening")
p1.tracks.append("song")
print(p2.tracks)    # ['song']  surprise!
```

The fix is to use `None` as the default and create a fresh list inside:

```python
class Playlist:
    def __init__(self, name, tracks=None):
        self.name = name
        self.tracks = [] if tracks is None else list(tracks)
```

Writing `list(tracks)` also makes a copy, so changing the playlist does not change the list the caller passed in.

## Many instances working together

A larger design often has one object that holds many others:

```python
class Fleet:
    def __init__(self):
        self.bikes = {}

    def add(self, bike):
        self.bikes[bike.bike_id] = bike

    def available(self):
        return sorted(i for i, b in self.bikes.items() if not b.rented)
```

The `Fleet` does not copy the bikes, it holds references to the same instances. If a bike is rented through the fleet or directly, the change is seen everywhere.

## Debugging tip

If two objects seem to change together, they are probably the **same** object, or they share a mutable default. Check with `a is b`, and look at `id(a)` and `id(b)`.

## Common mistakes

- Using a list or dictionary as a default argument.
- Relying on `__del__` for work that must always happen.
- Assuming `b = a` makes a copy. It just gives the same object a second name.
- Putting setup in a method you forget to call, instead of in `__init__`.
