Write these types.

- `Shape`: `area()` raises `NotImplementedError`.
- `Rect(width, height)`: `area()` is width times height.
- `Square(side)`: built from `Rect`, using the same side for both dimensions.
- `Circle(radius)`: `area()` is `3.14159 * radius * radius`.

Then write `total_area(shapes)` returning the sum of the areas of a list of shapes, rounded to 2 decimal places (0 for an empty list).

```python
total_area([Rect(2, 3), Square(2)])   # 10
```
