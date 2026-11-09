Write `word_frequencies(path)` that reads a text file and returns a dictionary of word counts, where words are compared without regard to capitalization and have all punctuation removed (so `"Tea,"`, `"tea"` and `"TEA!"` are one word). Anything that is empty after cleaning, such as a lone `"--"`, is not counted.

An apostrophe counts as punctuation: `"don't"` becomes `"dont"`.
