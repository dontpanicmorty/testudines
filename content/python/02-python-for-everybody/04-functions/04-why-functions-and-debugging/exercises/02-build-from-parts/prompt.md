A fitness app estimates the calories burned by walking as `steps * weight_kg * 0.0005`, then rounds the result to one decimal place. Write `walk_calories(steps, weight_kg)` that returns the rounded value. For tidiness, split the work into at least two small functions of your own, one to calculate and one to round (the tests only call `walk_calories`).

```python
walk_calories(10000, 70)    # 350.0
walk_calories(3333, 60)     # 100.0
```
