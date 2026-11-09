Write a base type `Member(name)` with a method `loan_limit()` returning 3, and a method `summary()` returning `"<name>: <limit>"` (using that member's own limit).

Then write `Student` and `Staff`, both built from `Member`. A `Student` has a limit of 5. A `Staff` has a limit of 10. Neither should repeat the `summary` code.

```python
Student("Ines").summary()    # "Ines: 5"
Member("Omar").summary()     # "Omar: 3"
```
