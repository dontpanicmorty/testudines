+++
id = "everybody.object-oriented-programming.inheritance"
title = "Inheritance"
minutes = 30
+++

# Inheritance

Sometimes one kind of thing is a special case of another. A student member of a library is still a member, but with a bigger loan limit. **Inheritance** lets a new class start from an existing one and change only what is different.

## Subclasses

The existing class is the **parent** (or base class, or superclass). The new class is the **child** (or subclass). Write the parent's name in parentheses:

```python
class Member:
    def __init__(self, name):
        self.name = name

    def loan_limit(self):
        return 3

    def describe(self):
        return f"{self.name} may borrow {self.loan_limit()} books"


class Student(Member):
    pass
```

`Student` has done nothing yet, but it already has everything `Member` has:

```python
s = Student("Ines")
print(s.describe())     # Ines may borrow 3 books
```

## Overriding a method

A child can **override** a method by defining one with the same name. Python looks in the child first.

```python
class Student(Member):
    def loan_limit(self):
        return 5

print(Student("Ines").describe())   # Ines may borrow 5 books
```

Notice that `describe` was never rewritten. It calls `self.loan_limit()`, and because `self` is a `Student`, Python picks the student's version. The same code behaves differently for different kinds of object. This idea is called **polymorphism** ("many shapes").

## Extending a method with super()

Often you do not want to replace the parent's work, just add to it. `super()` gives you the parent's version of a method.

```python
class Vehicle:
    def __init__(self, name, wheels):
        self.name = name
        self.wheels = wheels

    def describe(self):
        return f"{self.name} with {self.wheels} wheels"


class Trike(Vehicle):
    def __init__(self, name):
        super().__init__(name, 3)      # let the parent set up name and wheels
        self.bell = True

    def describe(self):
        return super().describe() + " and a bell"

print(Trike("Rosie").describe())   # Rosie with 3 wheels and a bell
```

If a child defines its own `__init__`, it must call `super().__init__(...)` so the parent's setup still happens. Forget it and the parent's attributes will be missing.

## Checking relationships

```python
t = Trike("Rosie")
print(isinstance(t, Trike))      # True
print(isinstance(t, Vehicle))    # True  (a Trike is a Vehicle)
print(issubclass(Trike, Vehicle))   # True
```

## A base class that asks to be filled in

A parent sometimes defines a method only to say "every child must provide this":

```python
class Shape:
    def area(self):
        raise NotImplementedError("subclasses must define area")
```

Code that works on any shape can then call `shape.area()` without caring which kind it is:

```python
def total_area(shapes):
    return sum(s.area() for s in shapes)
```

## When to use it

Inheritance is a good fit when the sentence "a Child **is a** Parent" sounds right: a student is a member, a trike is a vehicle. If it sounds odd ("a library is a book"?), the relationship is probably "has a", and you should put one object inside another as an attribute instead, as you did with the shelf of books.

## Vocabulary summary

- **class**: a blueprint for objects. **instance** / **object**: one thing built from it.
- **attribute**: data stored on an object. **method**: a function belonging to an object.
- **constructor** (`__init__`): runs when an instance is created. **destructor** (`__del__`): runs just before it is discarded.
- **inheritance**: a **subclass** reuses a **parent** class. **override**: redefine a method in the child. **`super()`**: reach the parent's version.

## Common mistakes

- Forgetting `super().__init__(...)` in a child's constructor.
- Overriding a method but with a different parameter list, so callers break.
- Using inheritance when "has a" is the true relationship.
- Writing `super.describe()` without the parentheses.
