A dictionary maps students to a score from 0 to 100. Write `bands(scores)` that groups the students by letter: `"A"` for 90 and up, `"B"` for 80 to 89, `"C"` for anything lower. Return a dictionary that maps each letter **that has at least one student** to an alphabetically sorted list of names.

```python
bands({"Ana": 95, "Ben": 82, "Cy": 90, "Dee": 40})
# {"A": ["Ana", "Cy"], "B": ["Ben"], "C": ["Dee"]}
```
