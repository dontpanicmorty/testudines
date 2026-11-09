Write `clean_sender(text)` that returns a standard form of a sender: if the text contains an address inside `<` and `>`, use only that address; strip spaces; convert to lowercase.

```python
clean_sender("Ines Ward <INES@Mail.Example.org>")   # "ines@mail.example.org"
clean_sender("  Omar@Club.example.com ")            # "omar@club.example.com"
```
