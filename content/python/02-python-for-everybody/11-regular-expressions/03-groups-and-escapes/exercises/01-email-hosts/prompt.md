Write `hosts(text)` that finds every email address in the text and returns a list of their domains (the part after the `@`), in order. An address is lowercase letters, digits or dots, then `@`, then a domain of lowercase letters, digits and dots. Trailing punctuation such as a comma or full stop at the end of a sentence is not part of the domain.

```python
hosts("write ana@example.org, or ben@mail.example.com")
# ["example.org", "mail.example.com"]
```
