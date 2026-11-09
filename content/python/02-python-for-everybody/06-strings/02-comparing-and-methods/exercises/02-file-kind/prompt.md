Write `file_kind(filename)`. Return a string describing the file based on how its name ends, ignoring upper and lower case:

- `.py` gives `"python"`
- `.txt` or `.md` gives `"text"`
- `.csv` gives `"table"`
- anything else gives `"unknown"`

`file_kind("Notes.MD")` returns `"text"`.
